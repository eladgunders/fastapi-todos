from typing import Union, Any

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, String, BigInteger, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, RelationshipProperty

from app.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    ...


class Priority(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False, unique=True)


class Category(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False)
    # Default categories are those where created_by_id is NULL,
    # indicating they are created by the system and are applicable to all users
    created_by_id = Column(GUID, ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint('name', 'created_by_id', name='unique_category'),
    )

    todos: RelationshipProperty = relationship(
        'Todo',
        secondary='todo_category',
        back_populates='categories',
        viewonly=True
    )


class Todo(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    is_completed = Column(Boolean(), nullable=False, default=False)
    content = Column(Text(), nullable=False)
    created_by_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    priority_id = Column(BigInteger(), ForeignKey('priority.id'), nullable=False)

    priority: RelationshipProperty = relationship('Priority', lazy='selectin')
    categories: RelationshipProperty = relationship(
        'Category',
        secondary='todo_category',
        back_populates='todos',
        lazy='selectin',
        viewonly=True
    )
    # just for adding todos_categories when adding a todo
    todos_categories: RelationshipProperty = relationship(
        'TodoCategory',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    def dict(self) -> dict:
        # adding todos_categories field to dict()
        # just update usage only
        todo_dict: dict[str, Union[int, str, bool]] = super().dict()
        todo_dict['todos_categories'] = self.todos_categories  # type: ignore[assignment]
        return todo_dict


class TodoCategory(Base):
    todo_id = Column(
        BigInteger(),
        ForeignKey('todo.id', ondelete='CASCADE'), primary_key=True
    )
    category_id = Column(
        BigInteger(),
        ForeignKey('category.id', ondelete='CASCADE'), primary_key=True
    )
