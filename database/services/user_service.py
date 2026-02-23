from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.user_repo import get_user_by_nickname, get_user_by_tg_id


async def get_current_chat_and_user(session: AsyncSession, message: Message):
    chat = await get_or_create_chat(session, message.chat.id)
    user = await get_user_by_tg_id(session, chat.id, message.from_user.id)
    return chat, user


async def require_current_chat_and_user(session: AsyncSession, message: Message):
    chat, user = await get_current_chat_and_user(session, message)
    
    if user is None:
        raise ValueError("вы не зарегистрированы. Сначала используйте /registerme.")
    
    return chat, user


async def ensure_nickname_unique(session: AsyncSession, chat_id: int, nickname: str | None) -> None:
    if not nickname:
        return
    
    existing = await get_user_by_nickname(session, chat_id, nickname)
    
    if existing:
        raise ValueError("этот никнейм уже занят другим пользователем.")
    