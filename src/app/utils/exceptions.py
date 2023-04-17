from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException


def exception_handler(func):
    @wraps(func)
    async def inner_function(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
    return inner_function
