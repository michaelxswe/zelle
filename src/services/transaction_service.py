from databases.postgresql.models import UserModel, TransactionModel
from decimal import Decimal
from exceptions import CustomException
from fastapi import status
from fastapi.responses import JSONResponse
from functools import lru_cache
from schemas.transaction import TransactionCreate, TransactionRead
from services.user_service import UserService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TransactionService:
    async def deposit(
            self,
            amount: Decimal,
            user_id: int,
            user_service: UserService,
            session: AsyncSession
    ):
        
        if amount <= 0:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Invalid amount.'
            )
        
        user = await user_service.get_user(id = user_id, session = session)
        user.balance += amount
        transaction = TransactionModel(
            user_id = user_id,
            receiver_id = None,
            amount = amount,
            message = f'You deposited ${amount}'
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(user)

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'detail': f'Successfully deposited ${amount}. Current balance is ${user.balance}.'}
        )

    async def withdraw(
            self,
            amount: Decimal,
            user_id: int,
            user_service: UserService,
            session: AsyncSession
    ):
        
        if amount <= 0:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Invalid amount.')
        
        user = await user_service.get_user(id = user_id, session = session)
        if user.balance < amount:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Insufficient balance.'
            )
        
        user.balance -= amount
        transaction = TransactionModel(
            user_id = user_id,
            receiver_id = None,
            amount = amount,
            message = f'You withdrew ${amount}'
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(user)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = { 'detail': f'Successfully withdrew ${amount}. Current balance is ${user.balance}.'}
        )

    async def transfer(
            self,
            data: TransactionCreate,
            user_id: int,
            user_service: UserService,
            session: AsyncSession
    ):
        query = select(UserModel).where(UserModel.phone == data.phone)
        receiver_res = await session.execute(query)
        receiver = receiver_res.scalar()

        if not receiver:
            raise CustomException(
                status_code = status.HTTP_404_NOT_FOUND,
                error = 'Invalid phone number'
            )

        user = await user_service.get_user(id = user_id, session = session)

        if user.balance < data.amount:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Insufficient balance.'
            )

        user.balance -= data.amount
        receiver.balance += data.amount
        transaction = TransactionModel(
            user_id = user_id,
            receiver_id = receiver.id,
            amount = data.amount,
            message = data.message,
        )

        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)
        await session.refresh(user)

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'detail': f'Successfully transfered ${data.amount} to {data.phone}. Your current balance is ${user.balance}.Your transaction id is {transaction.id}.'}
        )

    async def show_history(self, user_id: int, session: AsyncSession):
        res = []

        query = select(TransactionModel).where(TransactionModel.user_id == user_id)
        transactions_res = await session.execute(query)
        transactions = transactions_res.scalars()

        for transaction in transactions:
            query = select(UserModel).where(UserModel.id == transaction.receiver_id)
            user_res = await session.execute(query)
            user = user_res.scalar()
            if user:
                transaction_read = TransactionRead(
                    id = transaction.id,
                    phone = user.phone,
                    amount = transaction.amount,
                    message = transaction.message,
                    created_date = transaction.created_date,
                )
            else:
                transaction_read = TransactionRead(
                    id = transaction.id,
                    phone = None,
                    amount = transaction.amount,
                    message = transaction.message,
                    created_date = transaction.created_date,
                )
            res.append(transaction_read)

        return res

@lru_cache
def get_transaction_service():
    return TransactionService()