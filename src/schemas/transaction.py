from datetime import datetime
from decimal import Decimal
from exceptions.excs import AppException
from fastapi import status
from pydantic import BaseModel, ConfigDict, model_validator


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TransactionCreate(Transaction):
    phone: str
    amount: Decimal
    message: str | None = None

    @model_validator(mode="after")
    def populate_fields(self) -> "TransactionCreate":
        if self.amount <= 0:
            raise AppException(status_code=status.HTTP_400_BAD_REQUEST, message="Invalid amount.")

        return self


class TransactionRead(Transaction):
    id: int
    phone: str | None
    amount: Decimal
    message: str | None = None
    date: datetime
