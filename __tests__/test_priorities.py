import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_priorities(client: AsyncClient, user_token_headers: dict[str, str]):
    res = await client.get('/priorities', headers=user_token_headers)
    assert res.status_code == 200
    assert res.json() == []
