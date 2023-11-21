from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

from databases.pg import Base, get_engine

database_router = APIRouter(prefix="/api/databases", tags=["Database"])


@database_router.post("/create-pg")
async def create_pg(engine: AsyncEngine = Depends(get_engine)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Database is created successfully"},
    )
