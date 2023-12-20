from config import settings, Settings
from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession


def engine(settings: Settings = Depends(settings)):
    engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
    return engine


@lru_cache
def session_factory(engine: AsyncEngine = Depends(engine)):
    Session = async_sessionmaker(engine)
    return Session


async def session(Session: async_sessionmaker[AsyncSession] = Depends(session_factory)):
    async with Session() as session:
        yield session
