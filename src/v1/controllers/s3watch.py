# Standard Library
import json

# Third Party Library
from aws.s3 import S3
from aws_lambda_powertools.utilities.data_classes import S3Event


class WatchController:
    client = S3()

    def __init__(self, event: S3Event) -> None:
        self.event = event
        self._bucket_name = self.event.bucket_name
        self._object_key = self.event.object_key

    def find_json_file_body(self) -> str:
        json_object_key = self._object_key.split(".")[0] + ".json"
        json_data = self.client.fetch_object(self._bucket_name, json_object_key).decode("utf-8")
        return json.loads(json_data)
