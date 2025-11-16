from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session

from app.core.settings import settings
from app.repositories.authRepo import UserRepository
from app.schemas.users import TokenData, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(to_encode: dict, expire: datetime, token_type: str):
    to_encode.update({"exp": expire.timestamp(), "token_type": token_type})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return create_token(to_encode=to_encode, expire=expire, token_type="access_token")


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(days=15)
    return create_token(to_encode=to_encode, expire=expire, token_type="refresh_token")


async def verify_token(token: str, session: Session):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        userid = payload.get("sub")
        if userid is None:
            return None, False
        token_data = TokenData(
            user_id=userid, login="", token_type=payload.get("token_type")
        )
    except jwt.InvalidTokenError:
        return None, False

    user = UserRepository.get_user_by_id(session=session, id=int(token_data.user_id))  # type: ignore
    if user is None:
        return None, False
    user = UserOut(
        id=int(user.id),  # type: ignore
        username=str(user.username),
    )

    return TokenData(
        user_id=userid, login=user.username, token_type=payload.get("token_type")
    )
