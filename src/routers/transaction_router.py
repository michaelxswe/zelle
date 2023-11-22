from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import validate_token
from databases.pg import get_session
from schemas.transaction import TransactionCreate, TransactionRead
from schemas.user import UserRead
from services.transaction_service import TransactionService, get_transaction_service
from services.user_service import UserService, get_user_service

transaction_router = APIRouter(prefix="/api/transactions", tags=["Transaction"])


@transaction_router.post("/deposit")
async def deposit(
    amount: Decimal,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.deposit(
        amount=amount, user_id=user_id, user_service=user_service, session=session
    )


@transaction_router.post("/withdraw")
async def withdraw(
    amount: Decimal,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.withdraw(
        amount=amount, user_id=user_id, user_service=user_service, session=session
    )


@transaction_router.post("/transfer")
async def transfer(
    data: TransactionCreate,
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.transfer(
        data=data, user_id=user_id, user_service=user_service, session=session
    )


@transaction_router.get("/history", response_model=list[TransactionRead])
async def history(
    user_id: int = Depends(validate_token),
    transaction_service: TransactionService = Depends(get_transaction_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.history(user_id=user_id, session=session)
