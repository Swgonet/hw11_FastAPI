from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, extract
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy import func

from db import get_db

from models import Contacts
from schemas import ContactResponse, ContactCreateUpdate


app = FastAPI()

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = Contacts(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/", response_model=List[ContactResponse])
def get_contacts(q: Optional[str] = Query(None, alias="search"), db: Session = Depends(get_db)):
    if q:
        contacts = db.query(Contacts).filter((Contacts.first_name).contains(func.lower(q)) |
            func.lower(Contacts.last_name).contains(func.lower(q)) |
            func.lower(Contacts.email).contains(func.lower(q))
        ).all()
    else:
        contacts = db.query(Contacts).all()
    return contacts

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactCreateUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

@app.get("/contacts/birthdays/next-week", response_model=List[ContactResponse])
def get_birthdays_next_week(db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contacts).filter(
        extract('month', Contacts.birthday) == today.month,
        extract('day', Contacts.birthday) >= today.day,
        extract('day', Contacts.birthday) <= next_week.day
    ).all()
    return contacts