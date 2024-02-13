# mypy: ignore-errors

import boto3
import json


client = boto3.client("lambda")

s3 = boto3.client("s3")


def get_object_body(bucket: str, key: str) -> bytes:
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")


def invoke_lambda():
    payload = {
        "body": {
            "bucket_name": "aska-image-bucket-dev",
            "before": {"json_object_key":"id231321/1.json","image_object_key":"id231321/1.png"},
            "after": {"json_object_key":"id231321/2.json","image_object_key":"id231321/2.png"},
        }
    }

    response = client.invoke(
        FunctionName="aska-api-dev-ImageDiffHandler",
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=bytes(json.dumps(payload).encode()),
    )
    print(response["Payload"].read().decode("utf-8"))


if __name__ == "__main__":
    invoke_lambda()
