from fastapi import APIRouter, status, Depends

from app.api.deps import current_logged_user
from app.db.db_facade import DBFacade
from app.schemas.priority import Priority

router = APIRouter(
    prefix='/priorities',
    dependencies=[Depends(current_logged_user)],
    tags=['Priorities']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[Priority], status_code=status.HTTP_200_OK)
async def get_priorities():
    return await db_facade.get_priorities()
