import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient

from tests.conftest_utils import get_tests_data
from app.core.config import get_config


config = get_config()


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, status_code, res_body', [
    (None, 401, {'detail': 'Unauthorized'}),
    (
        lazy_fixture('user_token_headers'),
        200,
        get_tests_data()['categories'] + get_tests_data()['users'][0]['categories']
    )
], ids=['unauthorized access', 'authorized access'])
async def test_get_categories(
    client: AsyncClient,
    headers,
    status_code,
    res_body
):
    res = await client.get(f'{config.API_V1_STR}/categories', headers=headers)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, data, status_code, res_body', [
    (None, {'name': 'Work'}, 401, {'detail': 'Unauthorized'}),
    (lazy_fixture('user_token_headers'), {'name': 'Personal'}, 409, {'detail': 'category name already exists'}),
    (lazy_fixture('user_token_headers'), {'name': 'Chess'}, 409, {'detail': 'category name already exists'}),
    (lazy_fixture('user_token_headers'), {'name': 'Nintendo'}, 201, {'name': 'Nintendo', 'id': 5})
], ids=[
    'unauthorized access',
    'authorized access default existing category',
    'authorized access another users existing category',
    'authorized access non existing category'
])
async def test_add_category(
    client: AsyncClient,
    headers,
    data,
    status_code,
    res_body
):
    res = await client.post(f'{config.API_V1_STR}/categories', headers=headers, json=data)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, category_id, status_code, res_body', [
    (None, 1, 401, {'detail': 'Unauthorized'}),
    (lazy_fixture('user_token_headers'), 5, 404, {'detail': 'category does not exist'}),
    (
        lazy_fixture('user_token_headers'),
        1,
        403,
        {'detail': 'a user can not delete a category that was not created by him'}
    ),
    (
        lazy_fixture('user_token_headers'),
        4,
        403,
        {'detail': 'a user can not delete a category that was not created by him'}
    )
], ids=[
    'unauthorized access',
    'authorized access non existing category',
    'authorized access default existing category',
    'authorized access another users existing category'
])
async def test_delete_category_failure(
    client: AsyncClient,
    headers,
    category_id,
    status_code,
    res_body
):
    res = await client.delete(f'{config.API_V1_STR}/categories/{category_id}', headers=headers)
    assert res.status_code == status_code
    assert res.json() == res_body


@pytest.mark.asyncio
async def test_delete_category_success(
    client: AsyncClient,
    user_token_headers: dict[str, str]
):
    res = await client.delete(f'{config.API_V1_STR}/categories/3', headers=user_token_headers)
    assert res.status_code == 204
    assert len(res.content) == 0
