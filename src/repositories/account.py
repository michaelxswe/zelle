from databases.postgres.client import get_database_session
from databases.postgres.models import AccountModel
from fastapi import Depends
from schemas.account import AccountCreate, AccountUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AccountRepository:
    def __init__(self, session: AsyncSession = Depends(get_database_session)):
        self.session = session

    async def username_exist(self, username: str):
        query = select(AccountModel).where(AccountModel.username == username)
        response = await self.session.execute(query)
        account = response.scalar()
        return True if account else False

    async def create_account(self, account_data: AccountCreate):
        account = AccountModel(**account_data.model_dump())
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def get_account_by_id(self, account_id: int):
        query = select(AccountModel).where(AccountModel.id == account_id)
        response = await self.session.execute(query)
        account = response.scalar()
        return account

    async def get_account_by_credentials(self, username: str, password: str):
        query = select(AccountModel).where(AccountModel.username == username, AccountModel.password == password)
        response = await self.session.execute(query)
        account = response.scalar()
        return account

    async def update_account(self, account_data: AccountUpdate, account: AccountModel):
        for key, val in account_data.model_dump(exclude_unset=True).items():
            setattr(account, key, val)

        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def delete_account(self, account: AccountModel):
        await self.session.delete(account)
        await self.session.commit()
