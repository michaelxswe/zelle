from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from utils.settings import DATABASE_URL

engine = create_async_engine(url = DATABASE_URL, echo = True)
Session = async_sessionmaker(engine)

def get_engine():
    return engine

async def get_session():
    async with Session() as session:
        yield session