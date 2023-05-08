from typing import Final, Union
import contextlib
import json

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.auth import get_user_db, get_user_manager
from app.schemas import UserCreate
from app.models.tables import Priority, Category, Todo, TodoCategory, User


TESTS_DATA_FILE_PATH: Final[str] = 'todos/tests/tests_data.json'

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


def get_tests_data() -> dict[str, Union[list[dict], dict]]:
    with open(TESTS_DATA_FILE_PATH, 'r') as f:
        tests_data: dict[str, Union[list[dict], dict]] = json.load(f)
        return tests_data


async def insert_test_data(session: AsyncSession) -> None:
    tests_data = get_tests_data()
    priorities: list[Priority] = [
        Priority(name=p['name']) for p in tests_data['priorities']
    ]
    categories: list[Category] = [
        Category(name=c['name'], created_by_id=None) for c in tests_data['categories']
    ]
    session.add_all(priorities)
    session.add_all(categories)
    for user in tests_data['users']:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                db_user: User = await user_manager.create(
                    UserCreate(email=user['email'], password=user['password'])
                )
        users_categories: list[Category] = [
            Category(name=c['name'], created_by_id=db_user.id) for c in user['categories']
        ]
        session.add_all(users_categories)
        todos: list[Todo] = [
            Todo(
                content=t['content'],
                priority_id=t['priority_id'],
                created_by_id=db_user.id,
                todos_categories=[TodoCategory(category_id=c_id) for c_id in t['categories_ids']]
            ) for t in user['todos']
        ]
        session.add_all(todos)
    await session.commit()


async def get_user_token_headers(client: AsyncClient) -> dict[str, str]:
    tests_data = get_tests_data()
    login_data = {
        'username': tests_data['users'][0]['email'],
        'password': tests_data['users'][0]['password'],
    }
    res = await client.post('/auth/login', data=login_data)
    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


