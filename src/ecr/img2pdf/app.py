# Standard Library
import json

# Third Party Library
import boto3
import img2pdf
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field, ValidationError

logger = Logger()


class EventBody(BaseModel):
    bucket_name: str
    object_keys: list[str]
    is_dev: bool = Field(default=False)


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    logger.info(event)
    try:
        if isinstance(event.body, str):
            event_body_dict = json.loads(event.body)
        else:
            event_body_dict = event.body

        event_body = EventBody(**event_body_dict)
    except ValidationError as e:
        logger.error(e)
        raise e

    image_data = []
    for key in event_body.object_keys:
        response = boto3.client("s3").get_object(Bucket=event_body.bucket_name, Key=key)
        img_file_data = response["Body"].read()
        image_data.append(img_file_data)

    pdf_bytes = img2pdf.convert(image_data)  # type: ignore

    upload_bucket = "aska-tmp-dir"
    upload_object_key = "created_pdf.pdf"

    boto3.client("s3").put_object(Body=pdf_bytes, Bucket=upload_bucket, Key=upload_object_key)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Converted images to PDF and uploaded to S3",
                "objectKey": f"{upload_bucket}/{upload_object_key}",
            }
        ),
    }
