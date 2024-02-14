# Standard Library
from typing import Callable, TypeVar

# Third Party Library
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator

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

    # origin = event["headers"].get("origin")
    # if origin not in APP_API_CORS_ALLOWED_ORIGIN_LIST or not origin:
    #     raise UnauthorizedError("Invalid origin")
    response = handler(event, context)

    # headers
    response["headers"] = {  # type: ignore
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "http://localhost:5173",
    }

    return response
