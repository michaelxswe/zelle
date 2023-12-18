from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserCreate(User):
    username: str
    password: str
    phone: str


class UserUpdate(User):
    username: str | None = None
    password: str | None = None
    phone: str | None = None


class UserRead(User):
    id: int
    username: str
    password: str
    phone: str
    balance: Decimal
    created_date: datetime


class LoginCredential(User):
    username: str
    password: str
