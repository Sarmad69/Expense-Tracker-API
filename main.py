from fastapi import FastAPI
from schemas import ExpenseCreate, ExpenseResponse
from database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)