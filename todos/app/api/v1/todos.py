from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import conint

from app.core.db import get_async_session
from app.users.users import current_logged_user
from app.models.tables import User, Todo
from app.dal import db_service, GET_MULTI_DEFAULT_SKIP, GET_MULTI_DEFAULT_LIMIT, MAX_POSTGRES_INTEGER
from app.schemas import TodoRead, TodoInDB, TodoCreate, TodoUpdate, TodoUpdateInDB
from app.utils import exception_handler, get_open_api_response, get_open_api_unauthorized_access_response


router = APIRouter(
    prefix='/todos',
    dependencies=[
        Depends(current_logged_user),
        Depends(get_async_session)
    ],
    tags=['Todos']
)


@router.get(
    '',
    response_model=list[TodoRead],
    responses={status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response()}
)
async def get_todos(
    skip: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_SKIP,  # type: ignore[valid-type]
    limit: conint(ge=0, le=MAX_POSTGRES_INTEGER) = GET_MULTI_DEFAULT_LIMIT,  # type: ignore[valid-type]
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> Todo:
    return await db_service.get_todos(
        session,
        created_by_id=user.id,
        skip=skip,
        limit=limit
    )


@router.post(
    '',
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_400_BAD_REQUEST: get_open_api_response(
            {
                'Trying to connect duplicate categories or another users category': 'categories are not valid',
                'Trying to connect non existing priority': 'priority is not valid'
            }
        )

    }
)
@exception_handler
async def add_todo(
    todo_in: TodoCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> Todo:
    todo_in = TodoInDB(
        content=todo_in.content,
        priority_id=todo_in.priority_id,
        categories_ids=todo_in.categories_ids,
        created_by_id=user.id
    )
    return await db_service.add_todo(session, todo_in=todo_in)


@router.put(
    '/{todo_id}',
    response_model=TodoRead,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_400_BAD_REQUEST: get_open_api_response(
            {
                'Trying to connect duplicate categories or another users category': 'categories are not valid',
                'Trying to connect non existing priority': 'priority is not valid'
            }
        ),
        status.HTTP_403_FORBIDDEN: get_open_api_response(
            {'Trying to update another users todo':
             'a user can not update a todo that was not created by him'}
        ),
        status.HTTP_404_NOT_FOUND: get_open_api_response(
            {'Trying to update non existing todo': 'todo does not exists'}
        )
    }
)
@exception_handler
async def update_todo(
    todo_id: int,
    updated_todo: TodoUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> Todo:
    updated_todo = TodoUpdateInDB(
        id=todo_id,
        content=updated_todo.content,
        priority_id=updated_todo.priority_id,
        categories_ids=updated_todo.categories_ids,
        is_completed=updated_todo.is_completed,
        created_by_id=user.id
    )
    return await db_service.update_todo(session, updated_todo=updated_todo)


@router.delete(
    '/{todo_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: get_open_api_unauthorized_access_response(),
        status.HTTP_403_FORBIDDEN: get_open_api_response(
            {'Trying to update another users todo':
             'a user can not update a todo that was not created by him'}
        ),
        status.HTTP_404_NOT_FOUND: get_open_api_response(
            {'Trying to update non existing todo': 'todo does not exists'}
        )
    }
)
@exception_handler
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logged_user)
) -> None:
    await db_service.delete_todo(session, id_to_delete=todo_id, created_by_id=user.id)
