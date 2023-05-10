from typing import Final

import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient

from tests.conftest_utils import get_tests_data
from app.core.config import get_config


config = get_config()

API_TODOS_PREFIX: Final[str] = f'{config.API_V1_STR}/todos'


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, status_code, res_body', [
    (None, 401, {'detail': 'Unauthorized'}),
    (
        lazy_fixture('user_token_headers'),
        200,
        get_tests_data()['users'][0]['todos']
    )
], ids=['unauthorized access', 'authorized access'])
async def test_get_todos(
    client: AsyncClient,
    headers,
    status_code,
    res_body
):
    res = await client.get(API_TODOS_PREFIX, headers=headers)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, data, status_code, res_body', [
    (None, {}, 401, {'detail': 'Unauthorized'}),
    (
        lazy_fixture('user_token_headers'),
        {'content': 'Play Smash Bros', 'priority_id': 1, 'categories_ids': [1, 4]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        {'content': 'Play Smash Bros', 'priority_id': 1, 'categories_ids': [1, 1]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        {'content': 'Play Smash Bros', 'priority_id': 1, 'categories_ids': [1, 8]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        {'content': 'Play Smash Bros', 'priority_id': 4, 'categories_ids': [1, 2]},
        400,
        {'detail': 'priority is not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        {'content': 'Play Smash Bros', 'priority_id': 1, 'categories_ids': [1, 3]},
        201,
        {
            # id is 4 and not 3 because the 'authorized access non existing priority'
            # test case promotes the primary key.
            'id': 4,
            'is_completed': False,
            'content': 'Play Smash Bros',
            'priority': {'id': 1, 'name': 'Low'},
            'categories': [
                {
                    'id': 1,
                    'name': 'Personal'
                },
                {
                    'id': 3,
                    'name': 'Chess'
                }
            ]
        }
    ),
], ids=[
    'unauthorized access',
    'authorized access another users category',
    'authorized access duplicate valid category',
    'authorized access non existing category',
    'authorized access non existing priority',
    'authorized access valid data'
])
async def test_add_todo(
    client: AsyncClient,
    headers,
    data,
    status_code,
    res_body
):
    res = await client.post(API_TODOS_PREFIX, headers=headers, json=data)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, todo_id, data, status_code, res_body', [
    (None, 1, {}, 401, {'detail': 'Unauthorized'}),
    (
        lazy_fixture('user_token_headers'),
        3,
        {'content': 'Learn the sicilian', 'is_completed': True, 'priority_id': 3, 'categories_ids': [2]},
        404,
        {'detail': 'todo does not exist'}
    ),
    (
        lazy_fixture('user_token_headers'),
        2,
        {'content': 'Learn the sicilian', 'is_completed': True, 'priority_id': 3, 'categories_ids': [2]},
        403,
        {'detail': 'a user can not update a todo that was not created by him'}
    ),
    (
        lazy_fixture('user_token_headers'),
        1,
        {'content': 'Learn the sicilian opening', 'is_completed': True, 'priority_id': 2, 'categories_ids': [1, 4]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        1,
        {'content': 'Learn the sicilian opening', 'is_completed': True, 'priority_id': 2, 'categories_ids': [1, 1]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        1,
        {'content': 'Learn the sicilian opening', 'is_completed': True, 'priority_id': 2, 'categories_ids': [1, 8]},
        400,
        {'detail': 'categories are not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        1,
        {'content': 'Learn the sicilian opening', 'is_completed': True, 'priority_id': 5, 'categories_ids': [2]},
        400,
        {'detail': 'priority is not valid'}
    ),
    (
        lazy_fixture('user_token_headers'),
        1,
        {'content': 'Learn the sicilian', 'is_completed': True, 'priority_id': 1, 'categories_ids': [2]},
        200,
        {
            'id': 1,
            'is_completed': True,
            'content': 'Learn the sicilian',
            'priority': {'id': 1, 'name': 'Low'},
            'categories': [
                {
                    'id': 2,
                    'name': 'Work'
                }
            ]
        }
    )

], ids=[
    'unauthorized access',
    'authorized access non existing todo',
    'authorized access another users todo',
    'authorized access another users category',
    'authorized access duplicate valid category',
    'authorized access non existing category',
    'authorized access non existing priority',
    'authorized access valid data'
])
async def test_update_todo(
    client: AsyncClient,
    headers,
    todo_id,
    data,
    status_code,
    res_body
):
    res = await client.put(f'{API_TODOS_PREFIX}/{todo_id}', headers=headers, json=data)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, todo_id, status_code, res_body', [
    (None, 1, 401, {'detail': 'Unauthorized'}),
    (lazy_fixture('user_token_headers'), 5, 404, {'detail': 'todo does not exist'}),
    (
        lazy_fixture('user_token_headers'),
        2,
        403,
        {'detail': 'a user can not delete a todo that was not created by him'}
    )
], ids=[
    'unauthorized access',
    'authorized access non existing todo',
    'authorized access another users todo'
])
async def test_delete_todo_failure(
    client: AsyncClient,
    headers,
    todo_id,
    status_code,
    res_body
):
    res = await client.delete(f'{API_TODOS_PREFIX}/{todo_id}', headers=headers)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
async def test_delete_todo_success(
    client: AsyncClient,
    user_token_headers: dict[str, str]
):
    res = await client.delete(f'{API_TODOS_PREFIX}/1', headers=user_token_headers)
    assert res.status_code == 204
    assert len(res.content) == 0
