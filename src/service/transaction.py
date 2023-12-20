from database.postgresql.model import AccountModel, TransactionModel
from decimal import Decimal
from exception import HTTPException
from functools import lru_cache
from schema.transaction import TransactionCreate, TransactionHistory
from service.account import AccountService
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any


class TransactionService:
    async def deposit(
        self,
        amount: Decimal,
        claims: dict[str, Any],
        account_service: AccountService,
        session: AsyncSession,
    ):
        if amount <= 0:
            raise HTTPException(
                status_code=400,
                message="invalid amount",
            )

        account = await account_service.get_account(claims, session)

        account.balance += amount

        transaction = TransactionModel(account.id, None, "deposit", amount, None)
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        return transaction

    async def withdraw(
        self,
        amount: Decimal,
        claims: dict[str, Any],
        account_service: AccountService,
        session: AsyncSession,
    ):
        if amount <= 0:
            raise HTTPException(
                status_code=400,
                message="invalid amount",
            )

        account = await account_service.get_account(claims, session=session)
        if account.balance < amount:
            raise HTTPException(
                status_code=400,
                message="insufficient balance",
            )

        account.balance -= amount
        transaction = TransactionModel(
            account_id=account.id,
            recipient_account_id=None,
            amount=amount,
            mode="withdraw",
            message=None,
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction

    async def transfer(
        self,
        data: TransactionCreate,
        claims: dict[str, Any],
        account_service: AccountService,
        session: AsyncSession,
    ):
        account = await account_service.get_account(claims, session)

        query = select(AccountModel).where(AccountModel.id == data.recipient_account_id)

        response = await session.execute(query)

        recipient_account = response.scalar()

        if not recipient_account:
            raise HTTPException(
                status_code=404,
                message="recipient not found",
            )

        if recipient_account.id == account.id:
            raise HTTPException(
                status_code=400,
                message="recipient can't be yourself",
            )

        if account.balance < data.amount:
            raise HTTPException(
                status_code=400,
                message="insufficient balance",
            )

        account.balance -= data.amount
        recipient_account.balance += data.amount
        transaction = TransactionModel(
            account_id=account.id,
            recipient_account_id=recipient_account.id,
            mode="transfer",
            amount=data.amount,
            message=data.message,
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        return transaction

    async def history(self, claims: dict[str, Any], account_service: AccountService, session: AsyncSession):
        account = await account_service.get_account(claims, session)

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

        result = await session.execute(query, {"account_id": account.id})

        transaction_history = [TransactionHistory(**row._asdict()) for row in result]

        return transaction_history


@lru_cache
def transaction_service():
    return TransactionService()
