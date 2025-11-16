from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    @staticmethod
    def get_user_by_username(session: Session, username: str):
        stmt = select(User).where(User.username == username)  # type: ignore
        return session.scalars(stmt).first()

    @staticmethod
    def create_user(session: Session, user: UserCreate):
        user_db = User(
            username=user.username,
            hashed_password=pwd_context.hash(user.password),
        )
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db

    @staticmethod
    def get_user_by_id(session: Session, id: int):
        stmt = select(User).where(User.id == id)  # type: ignore
        return session.scalars(stmt).first()
