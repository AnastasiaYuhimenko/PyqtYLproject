from sqlalchemy.orm import Session

from app.repositories.authRepo import UserRepository
from app.schemas.users import UserCreate, UserGet, UserOut
from app.utils.auth import create_access_token, create_refresh_token, verify_password
from app.utils.settings import save_setting


class UserService:
    @staticmethod
    def register(session: Session, user: UserCreate):
        existing = UserRepository.get_user_by_username(session, user.username)
        if existing:
            return None, False

        new_user = UserRepository.create_user(session, user)

        return UserOut(id=new_user.id, username=new_user.username), True  # type: ignore

    @staticmethod
    def login(session: Session, user: UserGet):
        user_get = UserRepository.get_user_by_username(session, user.username)
        if not user_get:
            return "Такой пользователь не найден", False

        if not verify_password(user.password, user_get.hashed_password):
            return "Неверный пароль", False

        access_token = create_access_token(data={"sub": user_get.id})
        refresh_token = create_refresh_token(
            data={"sub": user_get.id, "token_type": "refresh_token"}
        )

        save_setting("access_token", access_token)
        save_setting("refresh_token", refresh_token)

        return UserOut(id=user_get.id, username=user_get.username), True  # type: ignore
