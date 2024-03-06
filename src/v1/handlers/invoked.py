# Standard Library

# Third Party Library
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from controllers.page import PageController

tracer = Tracer()
logger = Logger()

controller = PageController()


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info(event)
    controller.bulk_insert_pages(pages=event)
    return {"statusCode": 200, "body": event}
