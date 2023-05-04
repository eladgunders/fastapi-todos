from typing import Any

import humps
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy import inspect


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    # The following line is ignored by pylint even though it is like the documentation:
    # https://docs.sqlalchemy.org/en/14/orm/extensions/mypy.html#using-declared-attr-and-declarative-mixins
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return humps.depascalize(cls.__name__)

    def dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self) -> str:
        columns = [f'{col}: {getattr(self, col)}' for col in self.dict()]
        return f'{self.__class__.__name__}({", ".join(columns)})'

    def __str__(self) -> str:
        return self.__repr__()
