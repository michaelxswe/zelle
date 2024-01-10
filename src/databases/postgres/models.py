from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, text
from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC, TEXT, TIMESTAMP, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(VARCHAR(length=25), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(length=25))
    phone: Mapped[str] = mapped_column(VARCHAR(length=25), unique=True)
    balance: Mapped[Decimal] = mapped_column(NUMERIC(precision=10, scale=2), server_default="0.00", init=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("date_trunc('s', now())"), init=False
    )


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="cascade"))
    recipient_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="cascade"), nullable=True
    )
    mode: Mapped[str] = mapped_column(
        VARCHAR(length=25), CheckConstraint("mode in ('deposit', 'withdraw', 'transfer')")
    )
    amount: Mapped[Decimal] = mapped_column(NUMERIC(precision=10, scale=2), index=True)
    message: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("date_trunc('s', now())"), init=False
    )
