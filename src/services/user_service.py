from databases.postgresql.models import UserModel
from exceptions import CustomException
from fastapi import status
from functools import lru_cache
from schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    async def create_user(
            self,
            data: UserCreate,
            session: AsyncSession
    ):
        query = select(UserModel).where(UserModel.username == data.username)
        user_res = await session.execute(query)
        user = user_res.scalar()

        if user:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Username already exist.'
            )

        query = select(UserModel).where(UserModel.phone == data.phone)
        user_res = await session.execute(query)
        user = user_res.scalar()

        if user:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Phone number already exist.'
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
            raise CustomException(
                status_code = status.HTTP_404_NOT_FOUND,
                error = 'User not found.'
            )
        return user

@lru_cache
def get_user_service():
    return UserService()