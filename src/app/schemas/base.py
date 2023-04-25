from pydantic import BaseModel
from typing import Type, Union
from app.models.base import Base


class BaseInDB(BaseModel):
    class Config:
        orm_mode: bool = True
        orm_model: Union[Type[Base], None] = None

    def to_orm(self):
        if not self.Config.orm_model:
            raise AttributeError("Class has not defined Config.orm_model")
        return self.Config.orm_model(**dict(self))
