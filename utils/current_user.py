from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.user_repo import get_user


async def get_current_user(session: AsyncSession, message: Message):
    chat = await get_or_create_chat(session, message.chat.id)
    user = await get_user(session, chat.id, message.from_user.id)
    return user


async def get_current_user_with_chat_ids(session: AsyncSession, message: Message):
    chat = await get_or_create_chat(session, message.chat.id)
    user = await get_user(session, chat.id, message.from_user.id)
    return user, chat.id, message.from_user.id


async def require_current_user(session: AsyncSession, message: Message):
    user = await get_current_user(session, message)
    
    if user is None:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")
        return None
    
    return user