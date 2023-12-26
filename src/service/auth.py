from database.model import AccountModel
from exception import HTTPException
from fastapi import Request
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


async def get_auth_service(request: Request):
    return request.app.state.auth_service
