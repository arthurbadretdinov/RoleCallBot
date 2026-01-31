from sqlalchemy import select

from database.db import session_maker
from database.models.chat import Chat


async def get_or_create_chat(tg_chat_id):
    async with session_maker() as session:
        stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
        chat = await session.scalar(stmt)
        
        if not chat:
            chat = Chat(tg_chat_id=tg_chat_id)
            session.add(chat)
            await session.commit()
            await session.refresh(chat)

        return chat