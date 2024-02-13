# Standard Library
import functools
from typing import Callable, TypeVar

# Third Party Library
from aws_lambda_powertools import Logger

T = TypeVar("T")


def log_function_execution(
    logger: Logger = Logger(),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: T, **kwargs: T) -> T:
            # 開始ログ
            logger.debug(
                {"function": func.__name__, "args": args, "kwargs": kwargs, "status": "start"}
            )
            # 関数の実行
            result = func(*args, **kwargs)
            # 終了ログ
            logger.debug({"function": func.__name__, "result": result, "status": "end"})
            return result

        return wrapper

    return decorator
