# type: ignore

# Standard Library
import os

# Third Party Library
import boto3
import cv2
import numpy as np

# Local Library
from .image import ImageModel, JsonModel

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
            matches = bf.knnMatch(self.before_json.descriptors, self.after_json.descriptors, k=2)
            good_matches = []
            for m, n in matches:
                if m.distance < threshhold * n.distance:
                    good_matches.append(m)
            return good_matches
        except Exception as e:
            raise e

    def homography_matrix(self, min_matches: int) -> cv2.typing.MatLike:
        matches = self.matching(threshhold=THRESHOLD)
        if len(matches) < min_matches:
            src_pts = np.float32(
                [
                    (
                        self.before_json.key_points[m.queryIdx]["x"],
                        self.before_json.key_points[m.queryIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [
                    (
                        self.after_json.key_points[m.trainIdx]["x"],
                        self.after_json.key_points[m.trainIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            return M
        else:
            raise ValueError("The number of matches is less than the minimum number of matches.")

    def create_image_diff(self, matrix: list, threshold: int) -> None:
        before_image = self.before_image.image_data
        after_image = self.after_image.image_data
        threshold = 0 if threshold > 255 or 0 > threshold else threshold
        rows, cols = after_image.shape
        mask = np.ones((rows, cols), dtype=np.uint8)
        warped_mask = cv2.warpPerspective(mask, matrix, before_image.shape[1::-1])
        warped_after_image = cv2.warpPerspective(
            self.after_image, matrix, before_image.shape[1::-1]
        )
        warped_after_image[warped_mask == 0] = 255

        diff_image = cv2.absdiff(warped_after_image, before_image)
        _, threshdiff = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)
        threshdiff = 255 - threshdiff

        image_path = "/tmp/diff.png"
        cv2.imwrite(image_path, threshdiff)
        client.upload_file(
            Filename=image_path,
            Bucket="aska-tmp-dir",
            Key=f"{self.id}/diff_{self.page}.png",
            ExtraArgs={"ContentType": "image/png"},
        )
        os.remove(image_path)
