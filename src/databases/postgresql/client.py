from config import get_settings, Settings
from fastapi import Depends
from functools import lru_cache
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


@lru_cache
def get_engine(settings: Settings = Depends(get_settings)):
    engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
    return engine


@lru_cache
def get_session_factory(engine=Depends(get_engine)):
    Session = async_sessionmaker(engine)
    return Session


async def get_session(Session=Depends(get_session_factory)):
    async with Session() as session:
        yield session
