from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

from databases.pg import Base, get_engine
from middlewares.handle_error import ApplicationException

database_router = APIRouter(prefix="/api/databases", tags=["Database"])
from utils.settings import PASSWORD


@database_router.post("/pg")
async def create_pg(password: str, engine: AsyncEngine = Depends(get_engine)):
    if password != PASSWORD:
        raise ApplicationException(status_code=status.HTTP_401_UNAUTHORIZED, error="Invalid password.")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "Database is created successfully."},
    )
