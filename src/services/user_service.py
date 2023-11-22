from functools import lru_cache

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.handle_error import ApplicationException
from models.user_model import UserModel
from schemas.user import UserCreate


class UserService:
    async def create_user(self, data: UserCreate, session: AsyncSession):
        query = select(UserModel).where(UserModel.username == data.username)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if user:
            raise ApplicationException(
                status_code=status.HTTP_400_BAD_REQUEST, error="Username already exist."
            )

        query = select(UserModel).where(UserModel.phone == data.phone)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if user:
            raise ApplicationException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error="Phone number already exist.",
            )

        user = UserModel(**data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user(self, id: int, session: AsyncSession):
        query = select(UserModel).where(UserModel.id == id)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if not user:
            raise ApplicationException(
                status_code=status.HTTP_404_NOT_FOUND, error="User not found."
            )
        return user

    async def get_info(self, user_id: int, session: AsyncSession):
        query = select(UserModel).where(UserModel.id == user_id)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if not user:
            raise ApplicationException(
                status_code=status.HTTP_404_NOT_FOUND, error="User not found."
            )
        return user

    async def verify_sign_in_credentials(
        self, username: str, password: str, session: AsyncSession
    ):
        query = select(UserModel).where(UserModel.username == username)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if not user or user.password != password:
            raise ApplicationException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error="Invalid username or password.",
            )
        return user.id


@lru_cache
def get_user_service():
    return UserService()
