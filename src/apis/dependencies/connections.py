from ...db.connections import async_session, AsyncSession as Session

async def get_db() -> Session: # type: ignore
    async with async_session() as session:
        yield session # type: ignore