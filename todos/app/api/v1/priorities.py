from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.users import current_logged_user
from app.dal import db_service
from app.models.tables import Priority
from app.schemas import PriorityRead
from app.utils import get_open_api_unauthorized_access_response


router = APIRouter(
    prefix='/priorities',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Priorities']
)


@router.get(
    '',
    response_model=list[PriorityRead],
    responses={status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response()}
)
async def get_priorities(
    session: AsyncSession = Depends(get_async_session)
) -> Priority:
    return await db_service.get_priorities(session)
