import uuid
from pydantic import BaseModel
from typing import Optional


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategoryIn(BaseModel):
    name: str
    created_by_id: Optional[uuid.UUID]
