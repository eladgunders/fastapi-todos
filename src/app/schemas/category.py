import uuid
from pydantic import BaseModel
from typing import Optional

from app.schemas.base import BaseInDB
from app.models.tables import Category as CategoryModel


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


class CategoryInDB(BaseInDB, CategoryCreate):
    created_by_id: Optional[uuid.UUID]

    class Config(BaseInDB.Config):
        orm_model = CategoryModel


class Category(CategoryInDB):
    id: int
