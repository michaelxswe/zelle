from databases.postgresql.models import UserModel, TransactionModel
from decimal import Decimal
from exceptions.excs import AppException
from fastapi import status
from fastapi.responses import JSONResponse
from functools import lru_cache
from schemas.transaction import TransactionCreate, TransactionRead
from services.user_service import UserService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class TransactionService:
    async def deposit(
        self,
        amount: Decimal,
        user_id: int,
        user_service: UserService,
        session: AsyncSession,
    ):
        if amount <= 0:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid amount.",
            )

        user = await user_service.get_user(id=user_id, session=session)
        user.balance += amount
        transaction = TransactionModel(
            user_id=user_id,
            receiver_id=None,
            amount=amount,
            message=f"You deposited ${amount}",
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": f"Successfully deposited ${amount}. Current balance is ${user.balance}."
            },
        )

    async def withdraw(
        self,
        amount: Decimal,
        user_id: int,
        user_service: UserService,
        session: AsyncSession,
    ):
        if amount <= 0:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid amount.",
            )

        user = await user_service.get_user(id=user_id, session=session)
        if user.balance < amount:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Insufficient balance.",
            )

        user.balance -= amount
        transaction = TransactionModel(
            user_id=None,
            receiver_id=user_id,
            amount=amount,
            message=f"You withdrew ${amount}",
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": f"Successfully withdrew ${amount}. Current balance is ${user.balance}."
            },
        )

    async def transfer(
        self,
        data: TransactionCreate,
        user_id: int,
        user_service: UserService,
        session: AsyncSession,
    ):
        query = select(UserModel).where(UserModel.phone == data.phone)
        receiver_res = await session.execute(query)
        receiver = receiver_res.scalar()

        if not receiver:
            raise AppException(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Invalid phone number",
            )

        user = await user_service.get_user(id=user_id, session=session)

        if user.balance < data.amount:
            raise AppException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Insufficient balance.",
            )

        user.balance -= data.amount
        receiver.balance += data.amount
        transaction = TransactionModel(
            user_id=user_id,
            receiver_id=receiver.id,
            amount=data.amount,
            message=data.message,
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        await session.refresh(user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": f"Successfully transfered ${data.amount} to {data.phone}. Your current balance is ${user.balance}.Your transaction id is {transaction.id}."
            },
        )

    async def show_history(self, user_id: int, session: AsyncSession):
        # phone numbers of anyone this user_id has transaction with
        query = select(UserModel).where(UserModel.id == user_id)
        user_res = await session.execute(query)
        user = user_res.scalar()

        if not user:
            raise AppException(status_code=status.HTTP_404_NOT_FOUND, message="User not found.")
        
        query = text(
            """
            SELECT * FROM (
            
            SELECT t.id as id, u.phone as phone, -1 * t.amount as amount, t.message as message, t.created_date as date
            FROM transaction t
            JOIN "user" u ON u.id = t.receiver_id
            WHERE t.user_id = :user_id or t.user_id is null

            UNION ALL

            SELECT t.id as id, u.phone as phone, t.amount as amount, t.message as message, t.created_date as date
            FROM transaction t
            JOIN "user" u ON u.id = t.user_id
            WHERE t.receiver_id = :user_id or t.receiver_id is null
            
            ) AS combined
            ORDER BY combined.id DESC;
        
            """

        )

        result = await session.execute(query, {"user_id": user_id})

        transactions = [TransactionRead(**r._asdict()) for r in result]

        return transactions


@lru_cache
def get_transaction_service():
    return TransactionService()
