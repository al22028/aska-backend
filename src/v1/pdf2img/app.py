# Standard Library
import json
import os
import urllib.parse
from typing import TypeVar

# Third Party Library
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pdf2image import convert_from_bytes

logger = Logger()


AWS_IMAGE_BUCKET = "aska-image-bucket-dev"


client = boto3.client("s3")

T = TypeVar("T")


# TODO: Refactor this function to use AWS Lambda Powertools


def convert_to_images(id: str, pdf_file_data: bytes) -> None:
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    logger.info("Convert PDF to Images")
    images = convert_from_bytes(pdf_file_data)
    for i, image in enumerate(images):
        image_path = f"/tmp/{i+1}.png"
        image.save(image_path, "PNG")
        with open(image_path, "rb") as f:
            client.upload_fileobj(f, AWS_IMAGE_BUCKET, f"{id}/{i+1}.png")
            logger.info(f"Uploaded {image_path} to {AWS_IMAGE_BUCKET}/{id}/{i+1}.png")
    os.removedirs("/tmp")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    s3_event = event["Records"][0]["s3"]
    bucket_name = s3_event["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(s3_event["object"]["key"], encoding="utf-8")
    pdf_id, _ = object_key.split("/")
    response = client.get_object(Bucket=bucket_name, Key=object_key)
    pdf_file_data = response["Body"].read()
    convert_to_images(pdf_id, pdf_file_data)
    return {"statusCode": 200, "body": json.dumps({"message": "Converted PDF to Images"})}
