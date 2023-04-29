import asyncio

from app.core.db import create_all_entities


asyncio.run(create_all_entities())
