from functools import wraps
from typing import Callable, Any
from fastapi import status, HTTPException


class ResourceNotExists(Exception):
    pass


class Forbidden(Exception):
    pass


def exception_handler(f: Callable) -> Any:
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        except ResourceNotExists as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Forbidden as err:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err))
    return decorated
