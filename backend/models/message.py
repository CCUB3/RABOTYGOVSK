from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class MessageBase(SQLModel):
    text: str


class MessageOut(MessageBase):
    id: int | None = Field(default=None)
    sent_at: datetime
    owner: str


class MessageDB(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner: str