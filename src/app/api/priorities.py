from fastapi import APIRouter, Depends

from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas import PriorityRead

router = APIRouter(
    prefix='/priorities',
    dependencies=[Depends(current_logged_user)],
    tags=['Priorities']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[PriorityRead])
async def get_priorities():
    return await db_facade.get_priorities()
