from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC, TIMESTAMP, VARCHAR, TEXT
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class TransactionModel(Base):
    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    receiver_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'), nullable=True)
    amount: Mapped[Decimal] = mapped_column(NUMERIC(precision=10, scale=2), index=True)
    message: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('''date_trunc('s', now())'''), init=False)

class UserModel(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, init=False)
    username: Mapped[str] = mapped_column(VARCHAR(length=25), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(length=25))
    phone: Mapped[str] = mapped_column(VARCHAR(length=25), unique=True)
    balance: Mapped[Decimal] = mapped_column(NUMERIC(precision=10, scale=2),server_default='0.00',init=False)
    created_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('''date_trunc('s', now())'''), init=False)