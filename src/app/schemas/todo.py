import uuid
from pydantic import BaseModel

from app.schemas.priority import PriorityOut
from app.schemas.category import CategoryOut


class TodoBase(BaseModel):
    content: str


class TodoOut(TodoBase):
    id: int
    is_completed: bool
    priority: PriorityOut
    categories: list[CategoryOut]

    class Config:
        orm_mode = True


class TodoCreate(TodoBase):
    priority_id: int
    categories_ids: list[int]


class TodoInDB(TodoCreate):
    created_by_id: uuid.UUID
