import pytest
from httpx import AsyncClient  # pylint: disable=import-error


@pytest.mark.asyncio
async def test_priorities_without_credentials(client: AsyncClient):
    res = await client.get('/priorities')
    assert res.status_code == 401
    assert res.json() == {'detail': 'Unauthorized'}


@pytest.mark.asyncio
async def test_priorities_with_credentials(
    client: AsyncClient,
    user_token_headers: dict[str, str],
    initial_priorities: dict[str, list[dict]]
):
    res = await client.get('/priorities', headers=user_token_headers)
    assert res.status_code == 200
    assert res.json() == initial_priorities
