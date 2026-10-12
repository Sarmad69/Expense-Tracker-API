from fastapi import FastAPI, Depends, HTTPException
from decimal import Decimal
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas import ExpenseCreate, ExpenseResponse, ExpenseSummary
from database import engine, Base, get_db

import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

def apply_expense_filters(statement,
                          category: str | None = None,
                          min_amount: Decimal | None = None,
                          start_date: date | None = None,
                          end_date: date | None = None,
                          ):
    
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Invalid Date Range")

    if category is not None:
        statement = statement.where(models.Expense.category == category)

    if min_amount is not None:
        statement = statement.where(models.Expense.amount >= min_amount)

    if start_date is not None:
        statement = statement.where(models.Expense.date >= start_date)

    if end_date is not None:
        statement = statement.where(models.Expense.date <= end_date)

    return statement

@app.post("/expenses", response_model=ExpenseResponse)
def expense_create(expense: ExpenseCreate, db: Session = Depends(get_db)):

    new_expense = models.Expense(
        title = expense.title,
        amount = expense.amount,
        category = expense.category,
        date = expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(category: str | None = None,
                 min_amount: Decimal | None = None,
                 start_date: date | None = None,
                 end_date: date | None = None,
                 db: Session = Depends(get_db)
                ):

    statement = select(models.Expense)
    statement = apply_expense_filters(statement=statement,
                                      category=category,
                                      min_amount=min_amount,
                                      start_date=start_date,
                                      end_date=end_date)
    expenses = db.scalars(statement).all()

    return expenses

@app.get("/expenses/summary", response_model=ExpenseSummary)
def get_total(category: str | None = None,
              min_amount: Decimal | None = None,
              start_date: date | None = None,
              end_date: date | None = None,
              db: Session = Depends(get_db)
              ):

    statement = select(func.sum(models.Expense.amount))
    statement = apply_expense_filters(statement=statement,
                                      category=category,
                                      min_amount=min_amount,
                                      start_date=start_date,
                                      end_date=end_date)
    total = db.scalar(statement)
    
    if total is None:
        total = Decimal("0.00")

    return {"total": total}

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):

    statement = select(models.Expense).where(models.Expense.id == expense_id)
    expense = db.scalar(statement)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense Not Found")
    
    return expense

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_update: ExpenseCreate, db: Session = Depends(get_db)):
    statement = select(models.Expense).where(models.Expense.id == expense_id)
    expense = db.scalar(statement)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense Not Found")
        
    expense.title = expense_update.title
    expense.category = expense_update.category
    expense.amount = expense_update.amount
    expense.date = expense_update.date

    db.commit()
    db.refresh(expense)

    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    
    statement = select(models.Expense).where(models.Expense.id == expense_id)
    expense = db.scalar(statement)

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense Not Found")

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense Deleted Successfully"
    }