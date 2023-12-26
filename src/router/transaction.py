from auth.guard import validate_jwt
from database.manager import get_session
from decimal import Decimal
from fastapi import APIRouter, Depends
from schema.transaction import TransactionCreate, FinancialTransaction, TransactionHistory, FundTransfer
from service.account import AccountService, get_account_service
from service.transaction import TransactionService, get_transaction_service
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

router = APIRouter(prefix="/api/transaction", tags=["Transaction"])


@router.post("/deposit", response_model=FinancialTransaction, status_code=201)
async def deposit(
    amount: Decimal,
    claims: dict[str, Any] = Depends(validate_jwt),
    transaction_service: TransactionService = Depends(get_transaction_service),
    account_service: AccountService = Depends(get_account_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.deposit(amount, claims, account_service, session)


@router.post("/withdraw", response_model=FinancialTransaction, status_code=201)
async def withdraw(
    amount: Decimal,
    claims: dict[str, Any] = Depends(validate_jwt),
    transaction_service: TransactionService = Depends(get_transaction_service),
    account_service: AccountService = Depends(get_account_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.withdraw(amount, claims, account_service, session)


@router.post("/transfer", response_model=FundTransfer, status_code=201)
async def transfer(
    data: TransactionCreate,
    claims: dict[str, Any] = Depends(validate_jwt),
    transaction_service: TransactionService = Depends(get_transaction_service),
    account_service: AccountService = Depends(get_account_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.transfer(data, claims, account_service, session)


@router.post("/history", response_model=list[TransactionHistory], status_code=201)
async def history(
    claims: dict[str, Any] = Depends(validate_jwt),
    transaction_service: TransactionService = Depends(get_transaction_service),
    account_service: AccountService = Depends(get_account_service),
    session: AsyncSession = Depends(get_session),
):
    return await transaction_service.history(claims, account_service, session)
