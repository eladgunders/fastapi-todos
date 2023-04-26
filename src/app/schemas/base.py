from pydantic import BaseModel
from typing import Type, Union
from app.models.base import Base


class BaseInDB(BaseModel):
    """
    base schema for every schema that stored in DB.
    provides a default to_orm method for converting
    Pydantic objects to SQLAlchemy objects
    """
    class Config:
        orm_model: Union[Type[Base], None] = None

    def to_orm(self):
        if not self.Config.orm_model:
            raise AttributeError("Class has not defined Config.orm_model")
        return self.Config.orm_model(**dict(self))  # pylint: disable=not-callable
