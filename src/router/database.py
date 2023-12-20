from database.postgresql.manager import engine
from database.postgresql.model import Base
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/api/databases", tags=["Database"])


@router.post("/postgresql", status_code=200, response_model=None)
async def reset_postgresql(engine: AsyncEngine = Depends(engine)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
