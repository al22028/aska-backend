# type: ignore
# Standard Library
import json

# Third Party Library
import boto3
import cv2
import numpy as np
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="MatchingScoreCalculator")

client = boto3.client("s3")


ACC = 0.2


def score_similarity(desc_0, desc_1) -> float:
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(desc_0, desc_1)
    dist = [m.distance for m in matches]
    ret = sum(dist) / len(dist)
    return ret


def get_object_body(bucket: str, key: str) -> str:
    response = client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    bucket_name = event.body["bucket_name"]
    before_object_key, after_object_key = (
        event.body["before"]["json_object_key"],
        event.body["after"]["json_object_key"],
    )
    before_data = get_object_body(bucket_name, before_object_key)
    after_data = get_object_body(bucket_name, after_object_key)
    after_descripter = json.loads(after_data)["descriptors"]
    before_descriptor = json.loads(before_data)["descriptors"]
    desc_num_ave = int(len(after_descripter) + len(before_descriptor)) / 2
    desc_num = int(desc_num_ave * ACC)
    score = score_similarity(
        np.array(after_descripter[:desc_num], dtype=np.uint8),
        np.array(before_descriptor[:desc_num], dtype=np.uint8),
    )
    logger.info(f"Matching score: {score}")
    return {"statusCode": 200, "score": score}
