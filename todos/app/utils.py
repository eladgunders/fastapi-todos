from typing import Callable, Any, Type
from functools import wraps

from fastapi import status, HTTPException

from app.http_exceptions import ResourceNotExists, UserNotAllowed, ResourceAlreadyExists


def exception_handler(f: Callable) -> Any:
    exception_map: dict[Type[Exception], int] = {
        ValueError: status.HTTP_400_BAD_REQUEST,
        UserNotAllowed: status.HTTP_403_FORBIDDEN,
        ResourceNotExists: status.HTTP_404_NOT_FOUND,
        ResourceAlreadyExists: status.HTTP_409_CONFLICT,
    }

    exceptions: tuple[Type[Exception], ...] = tuple(exception_map.keys())

    @wraps(f)
    async def decorated(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        try:
            return await f(*args, **kwargs)
        except exceptions as err:
            exception_cls = type(err)
            status_code = exception_map[exception_cls]
            raise HTTPException(status_code=status_code, detail=str(err))
    return decorated
