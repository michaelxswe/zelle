from decimal import Decimal

from fastapi import APIRouter, Depends
from schemas.transaction import (
    FinancialTransaction,
    FundTransfer,
    TransactionCreate,
    TransactionHistory,
)
from services.transaction import TransactionService
from utils.auth import get_access_token

router = APIRouter(prefix="/v1", tags=["Transactions"])


@router.post("/transactions/deposit", response_model=FinancialTransaction, status_code=201)
async def deposit(
    amount: Decimal,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.deposit(amount, access_token)


@router.post("/transactions/withdraw", response_model=FinancialTransaction, status_code=201)
async def withdraw(
    amount: Decimal,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.withdraw(amount, access_token)


@router.post("/transactions/transfer", response_model=FundTransfer, status_code=201)
async def transfer(
    transaction_data: TransactionCreate,
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.transfer(transaction_data, access_token)


@router.get("/transactions/history", response_model=list[TransactionHistory], status_code=201)
async def history(
    access_token: str = Depends(get_access_token),
    transaction_service: TransactionService = Depends(),
):
    return await transaction_service.get_history(access_token)
