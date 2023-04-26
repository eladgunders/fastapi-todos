import uuid
from pydantic import BaseModel

from app.schemas.base import BaseInDB
from app.schemas.priority import PriorityRead
from app.schemas.category import CategoryRead
from app.models.tables import Todo, TodoCategory


class TodoBase(BaseModel):
    content: str


class TodoRead(TodoBase):
    id: int
    is_completed: bool
    priority: PriorityRead
    categories: list[CategoryRead]

    class Config:
        orm_mode = True


class TodoCreate(TodoBase):
    priority_id: int
    categories_ids: list[int]


class TodoInDB(BaseInDB, TodoCreate):
    created_by_id: uuid.UUID
    priority_id: int

    class Config(BaseInDB.Config):
        orm_model = Todo

    def to_orm(self):
        """
        converts categories_ids to todos_categories
        """
        orm_data = dict(self)
        categories_ids = orm_data.pop('categories_ids')
        todo_orm = self.Config.orm_model(**orm_data)
        todo_orm.todos_categories = [TodoCategory(category_id=c_id) for c_id in categories_ids]
        return todo_orm
