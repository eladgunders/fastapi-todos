from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, String, BigInteger, Boolean
from sqlalchemy.orm import RelationshipProperty, relationship

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

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Todo(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    is_completed = Column(Boolean(), nullable=False, default=False)
    content = Column(Text(), nullable=False)
    created_by_id = Column(GUID, ForeignKey('user.id'), nullable=False)
    priority_id = Column(BigInteger(), ForeignKey('priority.id'), nullable=False)

    created_by: RelationshipProperty = relationship('User')
    priority: RelationshipProperty = relationship('Priority')
    categories: RelationshipProperty = relationship('TodoCategory', back_populates='todo_id')

    def get_dict(self):
        return {
            'id': self.id,
            'is_completed': self.is_completed,
            'content': self.content,
            'created_by': self.created_by,
            'priority': self.priority.name
        }


class TodoCategory(Base):
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    todo_id = Column(BigInteger(), ForeignKey('todo.id'), nullable=False)
    category_id = Column(BigInteger(), ForeignKey('category.id'), nullable=False)

    todo: RelationshipProperty = relationship('Todo')
    category: RelationshipProperty = relationship('Category')
