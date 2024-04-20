from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from db import Base, engine


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String)
    phone_number = Column(Integer)
    birthday = Column(Date)
    dodatkovi_data = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)