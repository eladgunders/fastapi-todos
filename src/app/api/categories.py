from fastapi import APIRouter, status, Depends

from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas.category import Category

router = APIRouter(
    prefix='/categories',
    dependencies=[Depends(current_logged_user)],
    tags=['Categories']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[Category], status_code=status.HTTP_200_OK)
async def get_categories(user=Depends(current_logged_user)):
    return await db_facade.get_categories(user.id)
