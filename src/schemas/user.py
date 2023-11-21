from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, model_validator


class User(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class UserCreate(User):
    username: str
    password: str
    confirm_password: str = Field(exclude=True)
    premium: bool
    email: str

    @model_validator(mode="after")
    def populate_fields(self) -> "UserCreate":
        self.username = self.username.lower()
        self.email = self.email.lower()
        if self.password != self.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
            )

        return self


class UserRead(User):
    id: int
    username: str
    password: str
    premium: bool
    email: str
    balance: Decimal
    created_date: datetime
