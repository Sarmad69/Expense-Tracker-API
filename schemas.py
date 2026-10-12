from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal

class ExpenseCreate(BaseModel):

    title: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    date: date

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date):

        if value > date.today():
            raise ValueError("Date Cannot be in the Future")
        return value

class ExpenseResponse(BaseModel):

    id: int
    title: str
    amount: Decimal
    category: str
    date: date

class ExpenseSummary(BaseModel):

    total: Decimal