from config import Settings, get_settings
from database.client import get_database_client, DatabaseClient
from exception import HTTPException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/database", tags=["Database"])


@router.post("/reset/{database_key}", status_code=201, response_model=None)
async def reset(database_key: str, database_client: DatabaseClient = Depends(get_database_client), settings: Settings = Depends(get_settings)):
    if database_key != settings.DATABASE_KEY:
        raise HTTPException(status_code=401, message="invalid database key")
    
    await database_client.drop_tables()
    await database_client.create_tables()
