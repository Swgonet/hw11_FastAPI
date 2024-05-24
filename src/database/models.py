from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.database.db import Base, engine


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String)
    phone_number = Column(Integer)
    birthday = Column(Date)
    dodatkovi_data = Column(String, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship("User", back_populates="contacts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    contacts = relationship("Contacts", back_populates="user")

Base.metadata.create_all(bind=engine)