from datetime import datetime
from decimal import Decimal
from exceptions import CustomException
from fastapi import status
from pydantic import BaseModel, ConfigDict, model_validator

class Transaction(BaseModel):
    model_config = ConfigDict(extra = 'forbid', from_attributes = True)

class TransactionCreate(Transaction):
    phone: str
    amount: Decimal
    message: str | None = None

    @model_validator(mode = 'after')
    def populate_fields(self) -> 'TransactionCreate':
        if self.amount <= 0:
            raise CustomException(
                status_code = status.HTTP_400_BAD_REQUEST,
                error = 'Invalid amount.'
            )

        return self

class TransactionRead(Transaction):
    id: int
    phone: str | None
    amount: Decimal
    message: str | None = None
    created_date: datetime