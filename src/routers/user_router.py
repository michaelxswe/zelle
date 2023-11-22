from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import create_token, validate_token
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


@user_router.get("", response_model=UserRead)
async def get_info(
    user_id: int = Depends(validate_token),
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    return await service.get_info(user_id, session=session)


@user_router.post("/sign-in")
async def sign_in(
    username: str,
    password: str,
    session: AsyncSession = Depends(get_session),
    service: UserService = Depends(get_user_service),
):
    user_id = await service.verify_sign_in_credentials(
        username=username, password=password, session=session
    )
    token = create_token(user_id=user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"token_type": "bearer", "access_token": token},
    )
