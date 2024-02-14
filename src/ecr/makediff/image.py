# Standard Library
import json

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

    def __init__(self, bucket_name: str, object_key: str) -> None:
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = self.load_data()

    def load_data(self) -> bytes:
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=self.object_key,
        )
        return response["Body"].read()

    def image_data(self) -> np.ndarray:
        data = np.frombuffer(self.data, np.uint8)
        return cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
