# type: ignore
# Standard Library
import csv
import json
import os
from collections import deque
from io import StringIO

# Third Party Library
import boto3
import cv2
import numpy as np
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service="MatchingScoreCalculator")

client = boto3.client("s3")

AWS_TMP_BUCKET = os.environ["AWS_TMP_BUCKET"]

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


def listup_object_keys(bucket: str) -> list[str]:
    response = client.list_objects_v2(Bucket=bucket)
    content = response["Contents"]
    key_list = []
    for c in content:
        key_list.append(str(c["Key"]))
    return key_list


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    bucket_name = event.body["bucket_name"]
    before_id = event.body["before"]["json_object_key"].split("/")[0]
    after_id = event.body["after"]["json_object_key"].split("/")[0]

    before_json_datas = deque()
    after_json_datas = deque()
    key_list = listup_object_keys(bucket_name)
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    for key in key_list:
        id = key.split("/")[0]
        is_json = key.endswith(".json")
        if id == before_id and is_json:
            data = get_object_body(bucket=bucket_name, key=key)
            before_json_datas.append(data)
        if id == after_id and is_json:
            data = get_object_body(bucket=bucket_name, key=key)
            after_json_datas.append(data)

    for before_data in before_json_datas:
        score_list = deque()
        before_descriptor = json.loads(before_data)["descriptors"]
        for after_data in after_json_datas:
            after_descriptor = json.loads(after_data)["descriptors"]
            desc_num_ave = int(len(after_descriptor) + len(before_descriptor)) / 2
            desc_num = int(desc_num_ave * ACC)
            score = score_similarity(
                np.array(after_descriptor[:desc_num], dtype=np.uint8),
                np.array(before_descriptor[:desc_num], dtype=np.uint8),
            )
            score_list.append(score)
        csv_writer.writerow(list(score_list))

    # TODO: find best matching of pages
    csv_bytes = csv_buffer.getvalue().encode()
    client.put_object(
        Bucket=AWS_TMP_BUCKET,
        Key="matching_result.csv",
        Body=csv_bytes,
    )
    return {"statusCode": 200, "body": {"objectKey": "matching_result.csv"}}
