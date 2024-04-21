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