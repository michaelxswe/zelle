from database.manager import get_database_manager, DatabaseManager
from database.model import Base
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/database", tags=["Database"])


@router.post("/reset", status_code=200, response_model=None)
async def reset(database_manager: DatabaseManager = Depends(get_database_manager)):
    await database_manager.drop_all()
    await database_manager.create_all()
