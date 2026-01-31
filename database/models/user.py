from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("tg_user_id", "chat_id", name="uq_user_chat"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    nickname: Mapped[str] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text("TRUE"))