# Third Party Library
import cv2
import numpy as np


def extract_feature_points(img: np.ndarray) -> dict:
    """
    1枚の画像から特徴点を抽出する関数

    Args:
      img (ndarray): 画像のndarray形式データ

    Return:
      list:
        list[0] (cv2.Keypoint): 特徴点の座標等のデータのtuple
        list[1]               : 1つの特徴点に対する特徴量記述子のデータのリスト
    """
    detector = cv2.AKAZE_create()  # type: ignore

    kp, desc = detector.detectAndCompute(img, None)
    kpt = []
    # keypointをシリアライズ化してリストに格納
    for k in kp:
        kp_dict = keypoint_serializer(k)
        kpt.append(kp_dict)
    res = {"keypoints": kpt, "descriptors": desc.tolist()}
    return res


def keypoint_serializer(kp: cv2.KeyPoint) -> dict:
    """
    JSONでデータを扱いたいため、cv2.Keypointをjsonにdumpsできる形にdecodeする
    1つのcv2.Keypointからパラメータ x,y,size,angle,response,octave,calss_idを取りだす
    取り出したパラメータを辞書型にして返す

    Args:
      kp (cv2.KeyPoint) : デコードするcv2.KeyPoint型のデータ

    Return:
      dict : cv2.KeyPointのパラメータを持った辞書
    """

    return {
        "x": float(kp.pt[0]),
        "y": float(kp.pt[1]),
        "size": float(kp.size),
        "angle": float(kp.angle),
        "response": float(kp.response),
        "octave": int(kp.octave),
        "class_id": int(kp.class_id),
    }
