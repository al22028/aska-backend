# type: ignore
# Standard Library
import json

# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

# Local Library
from calculator import Calculator
from image import ImageModel, JsonModel

logger = Logger(service="ImageDiffCalculator")

MIN_MACHTES = 10
THRESHOLD = 200


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    bucket_name = event.body["bucket_name"]
    before_json_object_key, after_json_object_key = (
        event.body["before"]["json_object_key"],
        event.body["after"]["json_object_key"],
    )
    before_image_object_key, after_image_object_key = (
        event.body["before"]["image_object_key"],
        event.body["after"]["image_object_key"],
    )
    print(before_image_object_key)
    print(after_image_object_key)


    before_json = JsonModel(bucket_name, before_json_object_key)
    after_json = JsonModel(bucket_name, after_json_object_key)
    before_image = ImageModel(bucket_name, before_image_object_key, "tmp/before.png")
    after_image = ImageModel(bucket_name, after_image_object_key, "tmp/after.png")

    print(before_json)
    print(after_json)

    pdf_id, image_name = before_image_object_key.split("/")
    page, _ = image_name.split(".")

    calculator = Calculator(before_json, after_json, before_image, after_image, pdf_id, page)
    homography_matrix = calculator.homography_matrix(min_matches=MIN_MACHTES)
    calculator.create_image_diff(homography_matrix, THRESHOLD)
    return {"statusCode": 200, "body": json.dumps({"message": "Created and sdaved diff image"})}
