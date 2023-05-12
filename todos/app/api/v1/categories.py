from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import conint

from app.core.db import get_async_session
from app.users.users import current_logged_user
from app.dal import db_service, GET_MULTI_DEFAULT_SKIP, GET_MULTI_DEFAULT_LIMIT, MAX_POSTGRES_INTEGER
from app.schemas import CategoryCreate, CategoryRead, CategoryInDB
from app.models.tables import Category, User
from app.utils.exceptions import exception_handler

router = APIRouter(
    prefix='/categories',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Categories']
)


@router.get('', response_model=list[CategoryRead])
async def get_categories(
    # The following lines are ignored by mypy because:
    # error: Invalid type comment or annotation  [valid-type]
    # note: Suggestion: use conint[...] instead of conint(...)
    # even though it is like the documentation: https://docs.pydantic.dev/latest/usage/types/#arguments-to-conint
    skip: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_SKIP,  # type: ignore[valid-type]
    limit: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_LIMIT,  # type: ignore[valid-type]
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> list[Category]:
    return await db_service.get_categories(
        session,
        created_by_id=user.id,
        skip=skip,
        limit=limit
    )


@router.post('', response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
@exception_handler
async def add_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> Category:
    category_in = CategoryInDB(name=category_in.name, created_by_id=user.id)
    return await db_service.add_category(session, category_in=category_in)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
@exception_handler
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> None:
    await db_service.delete_category(session, id_to_delete=category_id, created_by_id=user.id)
