# Standard Library
from functools import wraps
from typing import Any, Callable, TypeVar

# Third Party Library
from database.base import Engine
from sqlalchemy.orm import Session, sessionmaker

T = TypeVar("T")
session_maker = sessionmaker(bind=Engine, expire_on_commit=False)


def with_session(func: Callable[..., T]) -> Callable[..., T]:
    """Execute function with session

    Args:
        func (Callable): Function

    Raises:
        e: Exception

    Returns:
        Callable: Function
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        """Execute function with session

        Raises:
            e: Exception

        Returns:
            T: Result
        """
        _session: Session = session_maker()
        try:
            result = func(session=_session, *args, **kwargs)
            _session.commit()
        except Exception as e:
            _session.rollback()
            raise e
        finally:
            _session.close()
        return result

    return wrapper
