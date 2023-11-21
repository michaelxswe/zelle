from functools import lru_cache

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user_model import UserModel
from schemas.user import UserCreate


class UserService:
    async def create_user(self, data: UserCreate, session: AsyncSession):
        query = select(UserModel).where(UserModel.username == data.username)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already found"
            )

        query = select(UserModel).where(UserModel.email == data.email)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already found"
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user


@lru_cache
def get_user_service():
    return UserService()
