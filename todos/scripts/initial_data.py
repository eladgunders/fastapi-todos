from typing import Final
import json

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Session
from app.models.tables import Priority, Category


INITIAL_DATA_FILE_PATH: Final[str] = 'todos/scripts/initial_data.json'


async def initiate_data(session: AsyncSession) -> None:
    with open(INITIAL_DATA_FILE_PATH, 'r') as f:
        initial_data_dict: dict[str, list[dict]] = json.load(f)
    priorities: list[Priority] = [
        Priority(name=p['name']) for p in initial_data_dict['priorities']
    ]
    categories: list[Category] = [
        Category(name=c['name'], created_by_id=None) for c in initial_data_dict['categories']
    ]
    session.add_all(priorities)
    session.add_all(categories)
    await session.commit()


async def main() -> None:
    async with Session() as session:
        await initiate_data(session)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
