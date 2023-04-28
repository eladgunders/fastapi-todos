from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.deps import get_async_session
from app.api.deps import current_logged_user
from app.dao import DBFacade
from app.schemas import CategoryCreate, CategoryRead, CategoryInDB
from app.utils import exception_handler

router = APIRouter(
    prefix='/categories',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Categories']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[CategoryRead])
async def get_categories(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    return await db_facade.get_categories(session, created_by_id=user.id)


@router.post('', response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
@exception_handler
async def add_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    category_in = CategoryInDB(name=category_in.name, created_by_id=user.id)
    return await db_facade.add_category(session, category_in=category_in)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
@exception_handler
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_logged_user)
):
    await db_facade.delete_category(session, id_to_delete=category_id, created_by_id=user.id)
