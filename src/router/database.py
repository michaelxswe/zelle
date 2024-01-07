from config import Settings, get_settings
from database.postgres.client import DatabaseClient, get_database_client
from exception_handler import HttpException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/v1", tags=["Database"])


@router.post("/database/postgres/reset/{database_key}", status_code=201, response_model=None)
async def reset(database_key: str, database_client: DatabaseClient = Depends(get_database_client), settings: Settings = Depends(get_settings)):
    if database_key != settings.DATABASE_KEY:
        raise HttpException(status_code=401)
    
    await database_client.drop_tables()
    await database_client.create_tables()
