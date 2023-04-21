from functools import wraps
from typing import Callable, Any
from fastapi import status, HTTPException


def exception_handler(f: Callable) -> Any:
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    return decorated
