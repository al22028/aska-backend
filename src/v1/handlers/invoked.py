# Standard Library

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source

tracer = Tracer()
logger = Logger()


@event_source(data_class=LambdaFunctionUrlEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: LambdaFunctionUrlEvent, context) -> dict[str, str | int]:
    return {"statusCode": 200, "body": event.body}
