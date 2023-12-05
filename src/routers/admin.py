from databases.postgresql.client import get_engine
from databases.postgresql.models import Base
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine

admin = APIRouter(prefix = '/api/admin', tags = ['Admin'])

@admin.post('/postgresql')
async def reset_postgresql(engine: AsyncEngine = Depends(get_engine)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {'detail': 'Database is reset successfully.'}
    )