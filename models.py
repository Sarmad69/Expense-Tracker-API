from database import Base
from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from decimal import Decimal

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(50))
    date: Mapped[date] = mapped_column(Date)