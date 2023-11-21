from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.pg import get_session
from schemas.user import UserCreate, UserRead
from services.user_service import UserService, get_user_service

user_router = APIRouter(prefix="/api/users", tags=["User"])


@user_router.post("", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    return await service.create_user(data=data, session=session)


@user_router.get("/{id}", response_model=UserRead)
async def get_user(
    id: int,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(id=id, session=session)
