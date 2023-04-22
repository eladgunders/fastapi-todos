import humps
from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import inspect


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return humps.depascalize(cls.__name__)

    def get_dict(self) -> Dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self) -> str:
        columns = [f'{col}: {getattr(self, col)}' for col in self._dict()]
        return f'{self.__class__.__name__}({", ".join(columns)})'

    def __str__(self) -> str:
        return self.__repr__()
