from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    