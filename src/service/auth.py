from database.postgresql.model import AccountModel
from exception import HTTPException
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    async def verify_account_credentials(self, username: str, password: str, session: AsyncSession):
        query = select(AccountModel).where(AccountModel.username == username)
        response = await session.execute(query)
        account = response.scalar()
        if not account or account.password != password:
            raise HTTPException(status_code=401, message="invalid username or password")

        return account.id


@lru_cache
def auth_service():
    return AuthService()
