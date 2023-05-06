import pytest
from pytest_lazyfixture import lazy_fixture
from httpx import AsyncClient

from tests.conftest_utils import get_tests_data


@pytest.mark.asyncio
@pytest.mark.parametrize('headers, status_code, res_body', [
    (None, 401, {'detail': 'Unauthorized'}),
    (lazy_fixture('user_token_headers'), 200, get_tests_data()['priorities'])
], ids=['unauthorized access', 'authorized access'])
async def test_get_priorities(
    client: AsyncClient,
    headers,
    status_code,
    res_body
):
    res = await client.get('/priorities', headers=headers)
    assert res.status_code == status_code
    assert res.json() == res_body
