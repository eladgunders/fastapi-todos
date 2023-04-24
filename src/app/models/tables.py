from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, String, BigInteger, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    ...


class Priority(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False, unique=True)


class Category(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False)
    # Default category are those where created_by_id is NULL,
    # indicating they are created by the system and are applicable to all users
    created_by_id = Column(GUID, ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint('name', 'created_by_id', name='unique_category'),
    )

    todos = relationship('Todo', secondary='todo_category', back_populates='categories')


class Todo(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    is_completed = Column(Boolean(), nullable=False, default=False)
    content = Column(Text(), nullable=False)
    created_by_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    priority_id = Column(BigInteger(), ForeignKey('priority.id'), nullable=False)

    priority = relationship('Priority', lazy='selectin')
    categories = relationship('Category', secondary='todo_category', back_populates='todos', lazy='selectin')


class TodoCategory(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    todo_id = Column(BigInteger(), ForeignKey('todo.id'), nullable=False)
    category_id = Column(BigInteger(), ForeignKey('category.id'), nullable=False)
