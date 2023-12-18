from databases.postgresql.models import UserModel
from exceptions.excs import AppException
from fastapi import status
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class LoginService:
    async def verify_credentials(self, username: str, password: str, session: AsyncSession):
        query = select(UserModel).where(UserModel.username == username)
        user_res = await session.execute(query)
        user = user_res.scalar()
        if not user or user.password != password:
            raise AppException(
                status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid username or password."
            )

        return user.id


@lru_cache
def get_login_service():
    return LoginService()
