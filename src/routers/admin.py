from databases.postgresql.client import get_engine
from databases.postgresql.models import Base
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from middlewares.handle_error import ApplicationException
from sqlalchemy.ext.asyncio import AsyncEngine
from utils.settings import PASSWORD

router = APIRouter(prefix = '/api/admin', tags = ['Admin'])

@router.post('/reset')
async def reset(password: str, engine: AsyncEngine = Depends(get_engine)):
    if password != PASSWORD:
        raise ApplicationException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            error = 'Invalid password.'
        )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {'detail': 'Database is reset successfully.'}
    )