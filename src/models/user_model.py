from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from databases.pg import Base


class UserModel(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    premium: Mapped[bool] = mapped_column(Boolean)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        server_default="0",
        init=False,
    )
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )
