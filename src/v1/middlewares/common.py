# Standard Library
from typing import Callable, TypeVar

# Third Party Library
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from config.settings import APP_API_CORS_ALLOWED_ORIGIN_LIST

logger = Logger()

T = TypeVar("T")


@lambda_handler_decorator
def handler_middleware(handler: Callable[..., T], event: dict, context: dict) -> T:
    """handler middleware

    Args:
        handler (Callable): lambda handler
        event (dict): lambda event
        context (dict): lambda context

    Returns:
        Callable: lambda handler response
    """
    body: dict | None = event["body"]
    if not body:
        body = {}

    logger.info("Request", extra={"event": event, "body": body})

    origin = event["headers"].get("origin")

    if not origin:
        logger.info("Origin", extra={"origin": origin})
        response = handler(event, context)
        logger.info("Response", extra={"response": response})
        return response

    logger.info("Origin", extra={"origin": origin})
    if origin not in APP_API_CORS_ALLOWED_ORIGIN_LIST:
        raise UnauthorizedError("Invalid origin")
    response = handler(event, context)

    # headers
    response["headers"] = {  # type: ignore
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": origin,
    }

    logger.info("Response", extra={"response": response})

    return response
