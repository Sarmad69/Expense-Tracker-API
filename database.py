from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine



DATABSE_URL = "sqlite:///./expenses.db"

engine = create_engine(
    DATABSE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

class Base(DeclarativeBase):
    pass