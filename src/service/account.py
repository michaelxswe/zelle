from auth.guard import create_access_token, validate_access_token
from config import Settings, get_settings
from exception import HttpException
from fastapi import Depends
from repository.account import AccountRepository
from schema.account import AccountCreate, AccountUpdate


class AccountService:
    def __init__(self, account_repository: AccountRepository = Depends(), settings: Settings = Depends(get_settings)):
        self.account_repository = account_repository
        self.settings = settings

    async def create_account(self, account_data: AccountCreate):
        if await self.account_repository.username_exist(account_data.username):
            raise HttpException(status_code=400, message="username already exist")

        return await self.account_repository.create_account(account_data)

    async def get_account_by_id(self, account_id: int):
        account = await self.account_repository.get_account_by_id(account_id)  # type: ignore
        if not account:
            raise HttpException(status_code=404, message="account not found")

        return account

    async def get_account_by_credentials(self, username: str, password: str):
        account = await self.account_repository.get_account_by_credentials(username, password)  # type: ignore
        if not account:
            raise HttpException(status_code=404, message="account not found")

        return account

    async def get_account_by_access_token(self, access_token: str):
        claims = validate_access_token(access_token, self.settings.SECRET_KEY, [self.settings.ALGORITHM])
        account_id = claims.get("account_id")

        account = await self.account_repository.get_account_by_id(account_id)  # type: ignore

        if not account:
            raise HttpException(status_code=404, message="account not found")

        return account

    async def process_sign_in(self, username: str, password: str):
        account = await self.get_account_by_credentials(username, password)
        access_token = create_access_token(account, self.settings.SECRET_KEY, self.settings.ALGORITHM)
        return access_token

    async def update_account(self, account_data: AccountUpdate, access_token: str):
        account = await self.get_account_by_access_token(access_token)
        return await self.account_repository.update_account(account_data, account)  # type: ignore

    async def delete_account(self, token: str):
        account = await self.get_account_by_access_token(token)
        await self.account_repository.delete_account(account)
