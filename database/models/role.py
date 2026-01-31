from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("chat_id", "name", name="uq_chat_role_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chats.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
