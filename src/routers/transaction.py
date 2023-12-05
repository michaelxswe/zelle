from auth.jwt import validate_token
from databases.postgresql.client import get_session
from decimal import Decimal
from fastapi import APIRouter, Depends
from schemas.transaction import TransactionCreate, TransactionRead
from services.transaction_service import TransactionService, get_transaction_service
from services.user_service import UserService, get_user_service
from sqlalchemy.ext.asyncio import AsyncSession

transaction = APIRouter(prefix = '/api/transactions', tags = ['Transaction'])

@transaction.post('/deposit')
async def deposit(
    amount: Decimal,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
):

    return await transaction_service.deposit(
        amount = amount,
        user_id = user_id,
        user_service = user_service,
        session = session
    )

@transaction.post('/withdraw')
async def withdraw(
    amount: Decimal,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
):

    return await transaction_service.withdraw(
        amount = amount,
        user_id = user_id,
        user_service = user_service,
        session = session
    )

@transaction.post('/transfer')
async def transfer(
    data: TransactionCreate,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session)
):

    return await transaction_service.transfer(
        data = data,
        user_id = user_id,
        user_service = user_service,
        session = session
    )

@transaction.get('/history', response_model=list[TransactionRead])
async def show_history(
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    session: AsyncSession = Depends(get_session)
):

    return await transaction_service.show_history(
        user_id = user_id,
        session = session
    )