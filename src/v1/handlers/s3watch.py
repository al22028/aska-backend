# Third Party Library
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import S3Event, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

from controllers.s3watch import WatchController

logger = Logger()
session = boto3.Session()
s3 = session.client("s3")

controller = WatchController()


@event_source(source=S3Event)
def lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    controller.extract_feature_point(event)
    return {"status_code": 200}
