from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from databases.pg import get_session
from schemas.transaction import TransactionCreate
from services.transaction_service import TransactionService, get_transaction_service
from services.user_service import UserService, get_user_service

transaction_router = APIRouter(prefix="/api/transactions", tags=["Transaction"])


@transaction_router.post("/deposit")
async def deposit(
    data: TransactionCreate,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.deposit(
        data=data, user_service=user_service, session=session
    )


@transaction_router.post("/transfer-money")
async def transfer_money(
    data: TransactionCreate,
    transaction_service: TransactionService = Depends(get_transaction_service),
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.transfer_money(
        data=data, user_service=user_service, session=session
    )
