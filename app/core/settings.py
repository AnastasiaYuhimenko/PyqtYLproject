import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(Path(__file__).parent.parent.parent, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120


settings = Settings()  # type: ignore
