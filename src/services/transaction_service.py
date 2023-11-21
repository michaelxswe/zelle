from functools import lru_cache

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.transaction_model import TransactionModel
from schemas.transaction import TransactionCreate
from services.user_service import UserService


class TransactionService:
    async def deposit(
        self, data: TransactionCreate, user_service: UserService, session: AsyncSession
    ):
        user = await user_service.get_user(id=data.user_id, session=session)
        user.balance += data.amount
        data.receiver_id = None
        transaction = TransactionModel(**data.model_dump())
        print(transaction)
        session.add(transaction)
        await session.commit()
        await session.refresh(user)
        return user

    async def transfer_money(
        self, data: TransactionCreate, user_service: UserService, session: AsyncSession
    ):
        if not data.receiver_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Receiver not found"
            )

        sender = await user_service.get_user(id=data.user_id, session=session)
        receiver = await user_service.get_user(id=data.receiver_id, session=session)

        if sender.balance < data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance"
            )

        sender.balance -= data.amount

        receiver.balance += data.amount

        transaction = TransactionModel(**data.model_dump())
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        return transaction


@lru_cache
def get_transaction_service():
    return TransactionService()
