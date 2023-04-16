from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, String, BigInteger, Boolean
from sqlalchemy.orm import declarative_base, RelationshipProperty, relationship

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    def get_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_superuser': self.is_superuser
        }


class Priority(Base):
    __tablename__ = 'priorities'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False, unique=True)

    def __repr__(self):
        return f'Priority(id_={self.id}, name={self.name})'

    def __str__(self):
        return self.__repr__()

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Category(Base):
    __tablename__ = 'categories'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)
    created_by_id = Column(GUID, ForeignKey('users.id'))

    def __repr__(self):
        return f'Priority(id_={self.id}, name={self.name}, created_by_id={self.created_by_id})'

    def __str__(self):
        return self.__repr__()

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Todo(Base):
    __tablename__ = 'todos'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    is_completed = Column(Boolean(), nullable=False, default=False)
    content = Column(Text(), nullable=False)
    created_by_id = Column(GUID, ForeignKey('users.id'), nullable=False)
    priority_id = Column(BigInteger(), ForeignKey('priorities.id'), nullable=False)

    created_by: RelationshipProperty = relationship('User')
    priority: RelationshipProperty = relationship('Priority')

    def __repr__(self):
        return f'Todo(id={self.id}, is_completed={self.is_completed}, content={self.content}, ' \
               f'created_by_id={self.created_by_id}, priority_id={self.priority_id})'

    def __str__(self):
        return self.__repr__()

    def get_dict(self):
        return {
            'id': self.id,
            'is_completed': self.is_completed,
            'content': self.content,
            'created_by': self.created_by,
            'priority': self.priority.name
        }


class TodoCategory(Base):
    __tablename__ = 'todos_categories'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    todo_id = Column(BigInteger(), ForeignKey('todos.id'), nullable=False)
    category_id = Column(BigInteger(), ForeignKey('categories.id'), nullable=False)

    todo: RelationshipProperty = relationship('Todo')
    category: RelationshipProperty = relationship('Category')

    def __repr__(self):
        return f'TodoCategory(id={self.id}, todo_id={self.todo_id}, category_id={self.category_id})'

    def __str__(self):
        return self.__repr__()
