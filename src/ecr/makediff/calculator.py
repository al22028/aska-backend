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
from PIL import Image
from pydantic import BaseModel
from scipy.sparse import coo_matrix
from sklearn.cluster import DBSCAN

AWS_IMAGE_BUCKET = os.environ["AWS_IMAGE_BUCKET"]
AWS_TMP_BUCKET = os.environ["AWS_TMP_BUCKET"]

client = boto3.client("s3")

MIN_MACHTES = 10


class Calculator:

    def __init__(
        self,
        before_json: JsonModel,
        after_json: JsonModel,
        before_image: ImageModel,
        after_image: ImageModel,
        version_id: str,
        page: str,
        params: BaseModel,
    ) -> None:
        self.before_json = before_json
        self.after_json = after_json
        self.before_image = before_image
        self.after_image = after_image
        self.id = version_id
        self.page = page
        self.diff_img = None
        self.export_path = None

        self.match_threshold = params.match_threshold
        self.threshold = params.threshold
        self.eps = params.eps
        self.min_samples = params.min_samples

    def matching(self, threshold: float) -> list[cv2.DMatch]:
        """2 枚の画像から得られた特徴量記述子の距離(ここではハミング距離)を総当たりで計算。近さが閾値以下になるようなマッチングのリストを返す。

        Args:
            threshold (float): 近さの閾値

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
                if m.distance < threshold * n.distance:
                    good_matches.append(m)
            return good_matches
        except Exception as e:
            raise e

    # TODO: Refactor this method
    def homography_matrix(self) -> cv2.typing.MatLike:
        matches = self.matching(threshold=self.match_threshold)
        if len(matches) <= MIN_MACHTES:
            raise ValueError("The number of matches is less than the minimum number of matches.")
        src_pts = np.float32(
            [
                (
                    self.after_json.key_points()[m.trainIdx]["x"],
                    self.after_json.key_points()[m.trainIdx]["y"],
                )
                for m in matches
            ]
        ).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [
                (
                    self.before_json.key_points()[m.queryIdx]["x"],
                    self.before_json.key_points()[m.queryIdx]["y"],
                )
                for m in matches
            ]
        ).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return M

    def create_image_diff(self, matrix: list, is_dev: bool) -> None:
        before_image = self.before_image.image_data()
        after_image = self.after_image.image_data()
        threshold = 0 if self.threshold > 255 or 0 > self.threshold else self.threshold
        rows, cols = after_image.shape
        mask = np.ones((rows, cols), dtype=np.uint8)
        warped_mask = cv2.warpPerspective(mask, matrix, before_image.shape[1::-1])
        warped_after_image = cv2.warpPerspective(after_image, matrix, before_image.shape[1::-1])
        warped_after_image[warped_mask == 0] = 255
        diff_image = cv2.absdiff(warped_after_image, before_image)
        _, threshdiff = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)
        threshdiff = 255 - threshdiff

        if is_dev:
            processing_image = Image.fromarray(warped_after_image.astype("uint8"))
            processing_buffer = io.BytesIO()
            processing_image.save(processing_buffer, format="PNG")
            processing_buffer.seek(0)
            client.upload_fileobj(
                Fileobj=processing_buffer,
                Bucket=AWS_TMP_BUCKET,
                Key=f"{self.id}/processing_{self.page}.png",
                ExtraArgs={"ContentType": "image/png"},
            )
            paramter_string = f"match_threshold:{self.match_threshold}, threhsold:{self.threshold},  eps:{self.eps},  min_samples:{self.min_samples}"
            cv2.putText(
                threshdiff,
                paramter_string,
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 0, 0),
                3,
                cv2.LINE_AA,
            )

        image = Image.fromarray(threshdiff.astype("uint8"))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        client.upload_fileobj(
            Fileobj=buffer,
            Bucket=AWS_TMP_BUCKET,
            Key=f"{self.id}/diff_{self.page}.png",
            ExtraArgs={"ContentType": "image/png"},
        )
        self.diff_img = threshdiff

    def image_to_clusters(self) -> None:
        img = self.diff_img
        transformed_image = np.where(img == 0, 1, 0)
        sparse_transformed_matrix = coo_matrix(transformed_image)
        data = np.vstack([sparse_transformed_matrix.col, sparse_transformed_matrix.row]).T
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(data)
        labels = db.labels_
        del db
        gc.collect()
        unique_labels = set(labels) - {-1}
        result = []
        for label in unique_labels:
            idx = labels == label
            p = data[idx]
            result.append(
                {
                    "maxX": int(p[:, 0].max()),
                    "maxY": int(p[:, 1].max()),
                    "minX": int(p[:, 0].min()),
                    "minY": int(p[:, 1].min()),
                }
            )

        client.put_object(
            Bucket=AWS_TMP_BUCKET,
            Key=f"{self.id}/clusters_{self.page}.json",
            Body=json.dumps(result).encode(),
        )
        self.export_path = f"{self.id}/clusters_{self.page}.json"
