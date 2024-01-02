from database.client import get_database_client, DatabaseClient
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/database", tags=["Database"])


@router.post("/reset", status_code=200, response_model=None)
async def reset(database_client: DatabaseClient = Depends(get_database_client)):
    await database_client.drop_tables()
    await database_client.create_tables()
