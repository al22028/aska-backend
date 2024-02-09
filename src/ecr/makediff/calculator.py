# type: ignore

# Third Party Library
import cv2
import numpy as np

# Local Library
from .image import ImageModel

THRESHOLD = 0.85


class Calculator:

    def __init__(self, before: ImageModel, after: ImageModel) -> None:
        self.before_image = before
        self.after_image = after

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
            matches = bf.knnMatch(self.before_image.descriptors, self.after_image.descriptors, k=2)
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
                        self.before_image.key_points[m.queryIdx]["x"],
                        self.before_image.key_points[m.queryIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [
                    (
                        self.after_image.key_points[m.trainIdx]["x"],
                        self.after_image.key_points[m.trainIdx]["y"],
                    )
                    for m in matches
                ]
            ).reshape(-1, 1, 2)
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            return M
        else:
            raise ValueError("The number of matches is less than the minimum number of matches.")
