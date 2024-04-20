from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:qwerty@localhost:5432/abc'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from models import Contacts
# from schemas import ContactResponse, ContactCreateUpdate
# from datetime import date, timedelta
# from sqlalchemy import func

# # Create an async engine
# ASYNC_DATABASE_URL = 'postgresql+asyncpg://postgres:qwerty@localhost:5432/abc'
# async_engine = create_async_engine(ASYNC_DATABASE_URL)

# # Create async session factory
# async_session_factory = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )

# app = FastAPI()

# # Dependency to get the async database session
# async def get_db():
#     async with async_session_factory() as session:
#         yield session

# ...

# # All your route handlers using async def
