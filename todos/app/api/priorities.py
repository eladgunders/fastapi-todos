from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.auth import current_logged_user
from app.dal import db_service
from app.models.tables import Priority
from app.schemas import PriorityRead

router = APIRouter(
    prefix='/priorities',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Priorities']
)


@router.get('', response_model=list[PriorityRead])
async def get_priorities(
    session: AsyncSession = Depends(get_async_session)
) -> Priority:
    return await db_service.get_priorities(session)
