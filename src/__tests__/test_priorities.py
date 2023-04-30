import json

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
# TODO: add cases
async def test_priorities(client: AsyncClient, user_token_headers: dict[str, str]):
    res_without_credentials = await client.get('/priorities')
    assert res_without_credentials.status_code == 401
    assert res_without_credentials.json() == {'detail': 'Unauthorized'}
    res_with_credentials = await client.get('/priorities', headers=user_token_headers)
    with open('app/scripts/initial_data.json', 'r') as f:
        initial_data_dict: dict[str, list[dict]] = json.load(f)
        priorities = initial_data_dict['priorities']
    assert res_with_credentials.status_code == 200
    assert res_with_credentials.json() == priorities
