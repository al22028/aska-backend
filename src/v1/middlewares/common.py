# Standard Library
from typing import Callable, Dict, TypeVar

# Third Party Library
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from config.settings import APP_API_CORS_ALLOWED_ORIGIN_LIST

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

    origin = event["headers"]["origin"]
    if origin not in APP_API_CORS_ALLOWED_ORIGIN_LIST:
        raise UnauthorizedError("Invalid origin")
    response = handler(event, context)

    # headers
    response["headers"]: Dict[str, list[str] | str] = {  # type: ignore
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": origin,
    }

    return response
