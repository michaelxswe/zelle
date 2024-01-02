from datetime import datetime
from decimal import Decimal
from exception import HTTPException
from pydantic import BaseModel, ConfigDict, model_validator


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TransactionCreate(Transaction):
    recipient_account_id: int
    amount: Decimal
    message: str | None = None

    @model_validator(mode="after")
    def populate_fields(self):
        if self.amount <= 0:
            raise HTTPException(status_code=400, message="invalid amount")

        return self


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
