from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactCreateUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: int
    birthday: date
    dodatkovi_data: Optional[str] = None


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: int
    birthday: date
    dodatkovi_data: Optional[str] = None


    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None