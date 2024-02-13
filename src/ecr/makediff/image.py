# Standard Library
import json
import os

# Third Party Library
import boto3
import cv2
import numpy as np


class JsonModel:
    client = boto3.client("s3")

    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.load_data()

    def load_data(self) -> dict:
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=self.object_key)
        except Exception as e:
            raise e
        self.data = json.loads(response["Body"].read().decode("utf-8"))
        return self.data

    def descriptors(self) -> dict:
        return self.data["descriptors"]

    def key_points(self) -> dict:
        return self.data["keypoints"]


class ImageModel:
    client = boto3.client("s3")

    def __init__(self, bucket_name: str, object_key: str, local_download_path: str) -> None:
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.local_download_path = local_download_path
        self.load_data()

    def load_data(self) -> None:
        try:
            self.client.download_file(
                Bucket=self.bucket_name, Key=self.object_key, Filename=self.local_download_path
            )
        except Exception as e:
            raise e

    def image_data(self) -> np.ndarray:
        img = cv2.imread(self.local_download_path)
        return img

    def delete_local_image(self) -> None:
        os.remove(self.local_download_path)


"""
todo
現状のImageModelはjsonデータをとってきている。
画像を加工して表示したいので、画像をfetchするmodelを作成
ImageModelはJsonModelにリネーム

Imageをfetchしてjsonにシリアライズしたほうが早いのか、IOのほうが早いのか、見極めどころさん
 - 実験して確かめるしかないのかな

makediff/app.py,image.py,calculator.pyを基本いじっていく感じ

画像をfetchする方法



"""
