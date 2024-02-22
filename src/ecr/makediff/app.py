# type: ignore
# Standard Library
import json
import time

# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from calculator import Calculator
from image import ImageModel, JsonModel
from pydantic import BaseModel, Field, ValidationError

logger = Logger(service="ImageDiffCalculator")


class ObjectKeys(BaseModel):
    json_object_key: str
    image_object_key: str


class Params(BaseModel):
    match_threshold: float
    threshold: int
    eps: float
    min_samples: int


class EventBody(BaseModel):
    bucket_name: str
    before: ObjectKeys
    after: ObjectKeys
    params: Params
    is_dev: bool = Field(default=False)


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    try:
        if isinstance(event.body, str):
            event_body_dict = json.loads(event.body)
        else:
            event_body_dict = event.body

        event_body = EventBody(**event_body_dict)
    except ValidationError as e:
        logger(e)
        raise e
    bucket_name = event_body.bucket_name
    before_json_object_key, after_json_object_key = (
        event_body.before.json_object_key,
        event_body.after.json_object_key,
    )
    before_image_object_key, after_image_object_key = (
        event_body.before.image_object_key,
        event_body.after.image_object_key,
    )

    IS_DEV = event_body.is_dev

    before_json = JsonModel(bucket_name, before_json_object_key)
    after_json = JsonModel(bucket_name, after_json_object_key)
    before_image = ImageModel(bucket_name, before_image_object_key)
    after_image = ImageModel(bucket_name, after_image_object_key)
    pdf_id, image_name = before_image_object_key.split("/")
    # TODO: Use decorator to log time
    page, _ = image_name.split(".")
    logger.info(f"start : {time.time()}")
    now = time.time()
    calculator = Calculator(
        before_json, after_json, before_image, after_image, pdf_id, page, event_body.params
    )
    homography_matrix = calculator.homography_matrix()
    logger.info(f"homography : {time.time() - now}")
    now = time.time()
    calculator.create_image_diff(homography_matrix, IS_DEV)
    logger.info(f"create image diff : {time.time() - now}")
    now = time.time()
    calculator.image_to_clusters()
    logger.info(f"image to cluster : {time.time() - now}")
    now = time.time()
    return {"statusCode": 200, "body": json.dumps({"objectKey": f"{str(calculator.export_path)}"})}
