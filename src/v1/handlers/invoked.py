# Standard Library

# Standard Library
import json

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import LambdaFunctionUrlEvent, event_source
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from schemas import LmabdaInvokePayloadSchema

tracer = Tracer()
logger = Logger()


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@event_source(data_class=LambdaFunctionUrlEvent)
def lambda_handler(event: LambdaFunctionUrlEvent, context: LambdaContext) -> dict:
    try:
        event = parse(json.loads(event.body), LmabdaInvokePayloadSchema)  # type: ignore
    except ValidationError as e:
        return {"statusCode": 400, "body": e.errors()}

    return {"statusCode": 200, "body": event.body}
