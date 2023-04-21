from fastapi import APIRouter, Depends

from app.api.deps import current_logged_user
from app.dao.db_facade import DBFacade
from app.schemas.todo import TodoOut


router = APIRouter(
    prefix='/todos',
    dependencies=[Depends(current_logged_user)],
    tags=['Todos']
)

db_facade = DBFacade.get_instance()


@router.get('', response_model=list[TodoOut])
async def get_todos(user=Depends(current_logged_user)):
    return await db_facade.get_todos(user.id)
