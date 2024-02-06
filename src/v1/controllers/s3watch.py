from aws_lambda_powertools.utilities.data_classes import S3Event
from aws.s3 import S3
import cv2
import numpy as np
import json
from features.keypoints import extract_feature_points


class WatchController:
    client = S3()

    def extract_feature_point(self, event: S3Event) -> dict:
        bucket_name = event.bucket_name
        object_key = event.object_key
        image_data = self.client.fetch_object(bucket_name, object_key)
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
        serialized_data = extract_feature_points(image)
        self.client.upload_object(
            bucket_name, f"{object_key.split('.')[0]}.json", json.dumps(serialized_data).encode()
        )
        return serialized_data
