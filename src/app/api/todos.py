from fastapi import APIRouter, Depends, status

from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas.todo import TodoOut, TodoInDB, TodoCreate
from app.utils.exceptions import exception_handler


router = APIRouter(
    prefix='/todos',
    dependencies=[Depends(current_logged_user)],
    tags=['Todos']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[TodoOut])
async def get_todos(user=Depends(current_logged_user)):
    return await db_facade.get_todos(user.id)


@router.post('', response_model=TodoOut, status_code=status.HTTP_201_CREATED)
@exception_handler
async def add_todo(todo_in: TodoCreate, user=Depends(current_logged_user)):
    todo = TodoInDB(
        content=todo_in.content,
        priority_id=todo_in.priority_id,
        categories_ids=todo_in.categories_ids,
        created_by_id=user.id
    )
    return await db_facade.add_todo(todo)
