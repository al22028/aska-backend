# Standard Library
import json
import os
from typing import TypeVar

# Third Party Library
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from pdf2image import convert_from_path

logger = Logger()


client = boto3.client("s3")

T = TypeVar("T")


def convert_to_images(pdf_file_path: str) -> None:
    logger.info("Convert PDF to Images")
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")

    images = convert_from_path(pdf_file_path)

    for i, image in enumerate(images):
        image_path = f"/tmp/{i+1}.png"
        image.save(image_path, "PNG")
        # with open(image_path, "rb") as f:
        #     client.upload_fileobj(f, AWS_POSTER_THUMBNAIL_BUCKET, f"{i}.png")
        # os.remove(image_path)
    print("tmp/1.png:", os.path.exists("/tmp/1.png"))


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    convert_to_images("K16611_after.pdf")
    return {"statusCode": 200, "body": json.dumps({"message": "Converted PDF to Images"})}
