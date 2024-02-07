# Standard Library
import json

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import S3Event, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from controllers.s3watch import WatchController

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@event_source(data_class=S3Event)
def lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    controller = WatchController(event)
    json_data = controller.find_json_file_body()
    print(json_data)
    return {
        "statusCode": 200,
        "body": json.dumps(json_data),
    }
