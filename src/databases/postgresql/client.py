from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = 'postgresql+asyncpg://postgres:0000@postgres:5432/postgres'

engine = create_async_engine(url = DATABASE_URL, echo = True)
Session = async_sessionmaker(engine)

def get_engine():
    return engine

async def get_session():
    async with Session() as session:
        yield session