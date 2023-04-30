import asyncio

from app.core.db import create_all_entities


if __name__ == '__main__':
    asyncio.run(create_all_entities())
