from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TransactionCreate(Transaction):
    recipient_account_id: int
    amount: Decimal
    message: str | None = None


class FinancialTransaction(Transaction):
    id: int
    mode: str
    amount: Decimal
    created_at: datetime


class FundTransfer(Transaction):
    id: int
    mode: str
    recipient_account_id: int
    amount: Decimal
    message: str | None
    created_at: datetime


class TransactionHistory(Transaction):
    id: int
    account_id: int | None
    mode: str
    amount: Decimal
    message: str | None
    created_at: datetime
