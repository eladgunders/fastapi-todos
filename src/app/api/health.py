import socket
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Response

from app.api.auth.deps import get_async_session, get_user_manager

router = APIRouter(
    prefix='/health',
    dependencies=[
        Depends(get_async_session),
        Depends(get_user_manager)
    ],
    tags=['Health']
)


@router.get('', status_code=status.HTTP_204_NO_CONTENT)
async def health(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        #  SELECT 1 is a simple SQL query used to test database connectivity
        await asyncio.wait_for(session.execute("SELECT 1"), timeout=1)
    except (asyncio.TimeoutError, socket.gaierror):
        #  socket.gaierror exception is raised when there is an error resolving a hostname. In this case,
        #  it is being used to handle network-related errors that may occur when attempting to connect to the database
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
