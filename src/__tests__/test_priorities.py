import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
# TODO: add cases
async def test_priorities(
    client: AsyncClient,
    user_token_headers: dict[str, str],
    get_initial_priorities: dict[str, list[dict]]
):
    res_without_credentials = await client.get('/priorities')
    assert res_without_credentials.status_code == 401
    assert res_without_credentials.json() == {'detail': 'Unauthorized'}
    res_with_credentials = await client.get('/priorities', headers=user_token_headers)
    assert res_with_credentials.status_code == 200
    assert res_with_credentials.json() == get_initial_priorities
