from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import validate_token
from databases.pg import get_session
from schemas.user import UserCreate, UserRead
from services.user_service import UserService, get_user_service

router = APIRouter(prefix="/api/users", tags=["User"])


@router.post("", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    return await service.create_user(data=data, session=session)


@router.get("", response_model=UserRead)
async def get_info(
    user_id: int = Depends(validate_token),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    return await service.get_info(user_id, session=session)