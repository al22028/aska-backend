# Standard Library
import json

# Third Party Library
import boto3


class ImageModel:
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
