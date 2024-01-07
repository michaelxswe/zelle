from decimal import Decimal

from config import Settings, get_settings
from exception_handler import HttpException
from fastapi import Depends
from repository.transaction import TransactionRepository
from schema.transaction import TransactionCreate
from service.account import AccountService


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository = Depends(),
        account_service: AccountService = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self.transaction_repository = transaction_repository
        self.account_service = account_service
        self.settings = settings

    def sufficient_balance_check(self, current_balance, demanded_fund):
        if current_balance < demanded_fund:
            raise HttpException(status_code=400, message="insufficient balance")

    def valid_amount_check(self, amount):
        if amount <= 0:
            raise HttpException(status_code=400, message="invalid amount")

    async def deposit(self, amount: Decimal, access_token: str):
        self.valid_amount_check(amount)
        account = await self.account_service.get_account_by_access_token(access_token)

        return await self.transaction_repository.deposit(account, amount)

    async def withdraw(self, amount: Decimal, access_token: str):
        self.valid_amount_check(amount)
        account = await self.account_service.get_account_by_access_token(access_token)

        if account.balance < amount:
            raise HttpException(status_code=400, message="insufficient balance")

        return await self.transaction_repository.withdraw(account, amount)

    async def transfer(self, transaction_data: TransactionCreate, access_token: str):
        if transaction_data.amount <= 0:
            raise HttpException(status_code=400, message="invalid amount")

        account = await self.account_service.get_account_by_access_token(access_token)
        self.sufficient_balance_check(account.balance, transaction_data.amount)
        recipient_account = await self.account_service.get_account_by_id(transaction_data.recipient_account_id)

        if account.id == recipient_account.id:
            raise HttpException(status_code=400, message="cant transfer money to yourself")

        return await self.transaction_repository.transfer(
            account, recipient_account, transaction_data.amount, transaction_data.message
        )

    async def get_history(self, access_token: str):
        account = await self.account_service.get_account_by_access_token(access_token)
        return await self.transaction_repository.get_history(account)
