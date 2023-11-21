from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URL = "postgresql+asyncpg://postgres:0000@localhost:5432/mx"
engine = create_async_engine(url=DATABASE_URL, echo=True)
Session = async_sessionmaker(engine)

def get_engine():
    return engine

async def get_session():
    async with Session() as session:
        yield session
