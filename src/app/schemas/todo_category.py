from pydantic import BaseModel

from app.schemas.category import CategoryOut


class TodoCategoryOut(BaseModel):
    category: CategoryOut

    class Config:
        orm_mode = True
