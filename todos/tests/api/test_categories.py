import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient

from tests.conftest_utils import get_tests_data


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
    res = await client.get('/categories', headers=headers)
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
    post_res = await client.post('/categories', headers=headers, json=data)
    assert post_res.status_code == status_code
    assert post_res.json() == res_body
