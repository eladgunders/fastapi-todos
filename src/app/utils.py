from typing import Callable, Any

from functools import wraps
from fastapi import status, HTTPException

from app.http_exceptions import ResourceNotExists, UserNotAllowed, ResourceAlreadyExists


def exception_handler(f: Callable) -> Any:
    @wraps(f)
    async def decorated(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        except UserNotAllowed as err:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err))
        except ResourceNotExists as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except ResourceAlreadyExists as err:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
    return decorated
