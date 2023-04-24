import uuid
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryOut(CategoryCreate):
    id: int

    class Config:
        orm_mode = True


class CategoryInDB(CategoryCreate):
    created_by_id: uuid.UUID
