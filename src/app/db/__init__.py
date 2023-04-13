from app.db.db_facade import DBFacade


def connect_to_databases():
    DBFacade.get_instance()


async def disconnect_from_databases():
    await DBFacade.get_instance().disconnect_from_databases()
