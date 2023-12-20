from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class Account(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AccountCreate(Account):
    username: str
    password: str
    phone: str


class AccountUpdate(Account):
    username: str | None = None
    password: str | None = None
    phone: str | None = None


class AccountRead(Account):
    id: int
    username: str
    password: str
    phone: str
    balance: Decimal
    created_at: datetime


class AccountCredentials(Account):
    username: str
    password: str
