# type: ignore
# Standard Library
import json

# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from calculator import Calculator
from image import ImageModel, JsonModel
from pydantic import BaseModel

logger = Logger(service="ImageDiffCalculator")

MIN_MACHTES = 10


class ObjectKeys(BaseModel):
    json_object_key: str
    image_object_key: str


class Params(BaseModel):
    threshold: float
    eps: float
    min_samples: int


class EventBody(BaseModel):
    bucket_name: str
    before: ObjectKeys
    after: ObjectKeys
    params: Params


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    # TODO: fixing validation check
    event_body = EventBody(event.body)

    bucket_name = event_body.bucket_name
    before_json_object_key, after_json_object_key = (
        event_body.before.json_object_key,
        event_body.after.json_object_key,
    )
    before_image_object_key, after_image_object_key = (
        event_body.before.image_object_key,
        event_body.after.image_object_key,
    )
    THRESHOLD = event_body.params.threshold
    EPS = event_body.params.eps
    MIN_SAMPLES = event_body.params.min_samples

    before_json = JsonModel(bucket_name, before_json_object_key)
    after_json = JsonModel(bucket_name, after_json_object_key)
    before_image = ImageModel(bucket_name, before_image_object_key)
    after_image = ImageModel(bucket_name, after_image_object_key)
    pdf_id, image_name = before_image_object_key.split("/")
    page, _ = image_name.split(".")

    calculator = Calculator(before_json, after_json, before_image, after_image, pdf_id, page)
    homography_matrix = calculator.homography_matrix(min_matches=MIN_MACHTES)
    calculator.create_image_diff(homography_matrix, THRESHOLD)
    calculator.image_to_clusters(EPS, MIN_SAMPLES)
    return {"statusCode": 200, "body": json.dumps({"message": "Created and sdaved diff image"})}
