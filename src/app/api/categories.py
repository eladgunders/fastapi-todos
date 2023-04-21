from fastapi import APIRouter, status, Depends

from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas.category import CategoryOut, CategoryIn

router = APIRouter(
    prefix='/categories',
    dependencies=[Depends(current_logged_user)],
    tags=['Categories']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[CategoryOut])
async def get_categories(user=Depends(current_logged_user)):
    return await db_facade.get_categories(user.id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def add_category(category: CategoryIn, user=Depends(current_logged_user)):
    category.created_by_id = user.id
    await db_facade.add_category(category)
