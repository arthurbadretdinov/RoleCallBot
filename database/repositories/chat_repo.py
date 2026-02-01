from sqlalchemy import select

from database.models.chat import Chat


async def get_or_create_chat(session, tg_chat_id):
    stmt = select(Chat).where(Chat.tg_chat_id == tg_chat_id)
    chat = await session.scalar(stmt)
    
    if not chat:
        chat = Chat(tg_chat_id=tg_chat_id)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)

    return chat