import asyncio
from db.config import create_all_entities


asyncio.run(create_all_entities())
