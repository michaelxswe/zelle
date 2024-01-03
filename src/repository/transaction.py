from database.client import get_database_session
from database.model import AccountModel, TransactionModel
from decimal import Decimal
from fastapi import Depends
from schema.transaction import TransactionHistory
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class TransactionRepository:
    def __init__(self, session: AsyncSession = Depends(get_database_session)):
        self.session = session

    async def deposit(self, account: AccountModel, amount: Decimal):
        account.balance += amount
        transaction = TransactionModel(account.id, None, "deposit", amount, None)
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        return transaction

    async def withdraw(self, account: AccountModel, amount: Decimal):
        account.balance -= amount
        transaction = TransactionModel(account.id, None, "withdraw", amount, None)
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        return transaction

    async def transfer(
        self, account: AccountModel, recipient_account: AccountModel, amount: Decimal, message: str | None
    ):
        account.balance -= amount
        recipient_account.balance += amount
        transaction = TransactionModel(
            account_id=account.id,
            recipient_account_id=recipient_account.id,
            mode="transfer",
            amount=amount,
            message=message,
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        return transaction

    async def get_history(self, account: AccountModel):
        query = text(
            """
            select id, amount, message, created_at,
                case
                    when account_id = :account_id then recipient_account_id
                    else account_id
                end as account_id,
                case
                    when account_id = :account_id and mode = 'transfer' then 'send'
                    when recipient_account_id = :account_id and mode = 'transfer' then 'receive'
                    else mode
                end as mode
            from transaction
            where account_id = :account_id or recipient_account_id = :account_id
            order by id desc;
            """
        )

        result = await self.session.execute(query, {"account_id": account.id})

        transaction_history = [TransactionHistory(**row._asdict()) for row in result]

        return transaction_history
