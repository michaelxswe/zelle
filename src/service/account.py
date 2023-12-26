from database.model import AccountModel
from exception import HTTPException
from fastapi import Request
from schema.account import AccountCreate, AccountUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class AccountService:
    async def create_account(self, data: AccountCreate, session: AsyncSession):
        query = select(AccountModel).where(AccountModel.username == data.username)
        response = await session.execute(query)
        account = response.scalar()

        if account:
            raise HTTPException(status_code=400, message="username already exist")

        account = AccountModel(**data.model_dump())

        session.add(account)
        await session.commit()
        await session.refresh(account)
        return account

    async def get_account(self, claims: dict[str, Any], session: AsyncSession):
        account_id = claims.get("account_id")
        query = select(AccountModel).where(AccountModel.id == account_id)
        response = await session.execute(query)
        account = response.scalar()

        if not account:
            raise HTTPException(status_code=404, message="account not found")

        return account

    async def update_account(self, data: AccountUpdate, claims: dict[str, Any], session: AsyncSession):
        account = await self.get_account(claims, session)

        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(account, key, val)

        await session.commit()
        await session.refresh(account)
        return account

    async def delete_account(self, claims: dict[str, Any], session: AsyncSession):
        account = await self.get_account(claims, session)

        await session.delete(account)
        await session.commit()


async def get_account_service(request: Request):
    return request.app.state.account_service
