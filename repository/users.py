from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import User
from schemas import UserCreate
from auth import auth_service

class UserRepository:

    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def create_user(user: UserCreate, db: Session):
        hashed_password = auth_service.get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            return None

repository_users = UserRepository()
