from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from databases.pg import Base


class TransactionModel(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), init=False
    )
