from pydantic import BaseModel
from typing import Optional

from app.schemas.priority import PriorityOut
from app.schemas.category import CategoryOut
from app.schemas.todo_category import TodoCategoryOut


class TodoOut(BaseModel):
    id: int
    is_completed: bool
    content: str
    priority: PriorityOut
    todos_categories: Optional[list[TodoCategoryOut]]  # exists in the orm model but to part of the instance
    categories: Optional[list[CategoryOut]]  # not exists in the orm model but part of the instance

    class Config:
        orm_mode = True

    @classmethod
    # removes - todos_categories, adds - categories
    def from_orm(cls, todo_orm):
        model = super().from_orm(todo_orm)
        model.categories = [ct.category for ct in model.todos_categories]
        delattr(model, 'todos_categories')
        return model
