# Standard Library

# Standard Library
from typing import Callable

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.data_classes import S3Event, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext
from controllers.processor import calculate_matching_score

logger = Logger()
tracer = Tracer()


@lambda_handler_decorator
def middleware(
    handler: Callable[[dict, LambdaContext], dict],
    event: dict,
    context: LambdaContext,
) -> dict:
    logger.info(event, context)
    response = handler(event, context)
    logger.info(response)
    return response


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@middleware
@event_source(data_class=S3Event)
def json_watch_lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    calculate_matching_score(event)
    return {
        "statusCode": 200,
    }


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@middleware
@event_source(data_class=S3Event)
def image_watch_lambda_handler(event: S3Event, context: LambdaContext) -> dict:
    return {
        "statusCode": 200,
    }
