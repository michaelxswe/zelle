from decimal import Decimal

from auth.guard import get_access_token
from fastapi import APIRouter, Depends
from schema.transaction import (
    FinancialTransaction,
    FundTransfer,
    TransactionCreate,
    TransactionHistory,
)
from service.transaction import TransactionService

router = APIRouter(prefix="/v1", tags=["Transaction"])


@router.post("/transaction/deposit", response_model=FinancialTransaction, status_code=201)
async def deposit(
    amount: Decimal,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.deposit(amount, access_token)


@router.post("/transaction/withdraw", response_model=FinancialTransaction, status_code=201)
async def withdraw(
    amount: Decimal,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.withdraw(amount, access_token)


@router.post("/transaction/transfer", response_model=FundTransfer, status_code=201)
async def transfer(
    transaction_data: TransactionCreate,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.transfer(transaction_data, access_token)


@router.get("/transaction/history", response_model=list[TransactionHistory], status_code=201)
async def history(
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.get_history(access_token)
