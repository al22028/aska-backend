# type: ignore
# Standard Library

# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

# Local Library
from .calculator import Calculator
from .image import ImageModel

logger = Logger(service="ImageDiffCalculator")

MIN_MACHTES = 10


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    bucket_name = event.body["bucket_name"]
    before_object_key, after_object_key = event.body["before"], event.body["after"]
    before_image = ImageModel(bucket_name, before_object_key)
    after_image = ImageModel(bucket_name, after_object_key)
    calculator = Calculator(before_image, after_image)
    homography_matrix = calculator.homography_matrix(min_matches=MIN_MACHTES)

    return {"statusCode": 200, "score": "hello"}
