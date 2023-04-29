import asyncio

from app.core.db import create_all_entities


loop = asyncio.get_event_loop()
loop.run_until_complete(create_all_entities())
