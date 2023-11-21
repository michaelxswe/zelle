from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, model_validator


class Transaction(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class TransactionCreate(Transaction):
    user_id: int
    receiver_id: int | None = None
    amount: Decimal
    message: str | None = None

    @model_validator(mode="after")
    def populate_fields(self) -> "TransactionCreate":
        if self.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid amount"
            )

        if self.receiver_id and self.user_id == self.receiver_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot send money to yourself",
            )

        return self


class TransactionRead(Transaction):
    id: int
    user_id: int
    receiver_id: int | None = None
    amount: Decimal
    message: str | None = None
    created_date: datetime
