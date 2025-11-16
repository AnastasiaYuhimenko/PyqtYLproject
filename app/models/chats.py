from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    member = "member"


class Chat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: list[int] = Field(default_factory=list, sa_column=Column(JSON))


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: int = Field(foreign_key="user.id")
    send_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    text: str
    img: Optional[str] = None
    user2: int
