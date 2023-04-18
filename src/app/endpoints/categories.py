from fastapi import APIRouter, status, Depends

from db.user import current_logged_user
from app.db.dao.db_facade import DBFacade
from app.db.types.category import CategoryType

router = APIRouter(
    prefix='/categories',
    dependencies=[Depends(current_logged_user)],
    tags=['Categories']
)

db_facade = DBFacade.get_instance()


@router.get('', status_code=status.HTTP_200_OK)
async def get_categories(user=Depends(current_logged_user)) -> list[CategoryType]:
    return await db_facade.get_categories(user.id)
