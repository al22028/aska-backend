# type: ignore

# Standard Library
import gc
import io
import json
import os

# Third Party Library
import boto3
import cv2
import numpy as np
from image import ImageModel, JsonModel
from scipy.sparse import coo_matrix
from sklearn.cluster import DBSCAN

AWS_IMAGE_BUCKET = os.environ["AWS_IMAGE_BUCKET"]

client = boto3.client("s3")


THRESHOLD = 0.85


class Calculator:

    def __init__(
        self,
        before_json: JsonModel,
        after_json: JsonModel,
        before_image: ImageModel,
        after_image: ImageModel,
        id: str,
        page: str,
    ) -> None:
        self.before_json = before_json
        self.after_json = after_json
        self.before_image = before_image
        self.after_image = after_image
        self.id = id
        self.page = page
        self.diff_img = None

    def matching(self, threshhold: float) -> list[cv2.DMatch]:
        """2 枚の画像から得られた特徴量記述子の距離(ここではハミング距離)を総当たりで計算。近さが閾値以下になるようなマッチングのリストを返す。

        Args:
            threshhold (float): 近さの閾値

        Raises:
            e: 計算上でのエラー

        Returns:
            list[cv2.DMatch]: マッチングのリスト
        """
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        try:
            matches = bf.knnMatch(
                np.array(self.before_json.descriptors(), dtype=np.uint8),
                np.array(self.after_json.descriptors(), dtype=np.uint8),
                k=2,
            )
            good_matches = []
            for m, n in matches:
                if m.distance < threshhold * n.distance:
                    good_matches.append(m)
            return good_matches
        except Exception as e:
            raise e

    def homography_matrix(self, min_matches: int) -> cv2.typing.MatLike:
        matches = self.matching(threshhold=THRESHOLD)
        if len(matches) > min_matches:
            src_pts = np.float32(
                [
                    (
                        self.before_json.key_points()[m.queryIdx]["x"],
                        self.before_json.key_points()[m.queryIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [
                    (
                        self.after_json.key_points()[m.trainIdx]["x"],
                        self.after_json.key_points()[m.trainIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            return M
        else:
            raise ValueError("The number of matches is less than the minimum number of matches.")

    def create_image_diff(self, matrix: list, threshold: int) -> None:
        before_image = self.before_image.image_data()
        after_image = self.after_image.image_data()
        threshold = 0 if threshold > 255 or 0 > threshold else threshold
        rows, cols = after_image.shape
        mask = np.ones((rows, cols), dtype=np.uint8)
        warped_mask = cv2.warpPerspective(mask, matrix, before_image.shape[1::-1])
        warped_after_image = cv2.warpPerspective(after_image, matrix, before_image.shape[1::-1])
        warped_after_image[warped_mask == 0] = 255

        diff_image = cv2.absdiff(warped_after_image, before_image)
        _, threshdiff = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)
        threshdiff = 255 - threshdiff
        buffer = io.BytesIO()
        np.save(buffer, threshdiff)
        buffer.seek(0)
        client.upload_fileobj(
            Fileobj=buffer,
            Bucket="aska-tmp-dir",
            Key=f"{self.id}/diff_{self.page}.png",
            ExtraArgs={"ContentType": "image/png"},
        )
        self.diff_img = threshdiff

    def image_to_clusters(self, eps: float, min_samples: int) -> None:
        data = []
        img = self.diff_img
        transformed_image = np.where(img == 0, 1, 0)
        sparse_transformed_matxi = coo_matrix(transformed_image)
        for i in range(len(sparse_transformed_matxi.row)):
            m = sparse_transformed_matxi.col[i]
            n = sparse_transformed_matxi.row[i]
            data.append([m, n])

        np_data = np.array(data)

        db = DBSCAN(eps=eps, min_samples=min_samples).fit(np_data)
        labels = db.labels_

        del db, data
        gc.collect()

        unique_labels = np.unique(labels[labels != -1])
        result = {}
        for i in unique_labels:
            idx = np.where(labels == i)
            p = np_data[idx]
            result[str(i)] = {
                "position": {
                    "max_x": int(np.max(p[:, 0])),
                    "max_y": int(np.max(p[:, 1])),
                    "min_x": int(np.min(p[:, 0])),
                    "min_y": int(np.min(p[:, 1])),
                }
            }
        client.put_object(
            Bucket="aska-tmp-dir",
            Key=f"{self.id}/clusters_{self.page}.json",
            Body=json.dumps(result).encode(),
        )
