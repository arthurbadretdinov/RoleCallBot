from sqlalchemy import select

from database.db import session_maker
from database.models.user import User
            

async def get_user(chat_id, tg_user_id):
    async with session_maker() as session:
        stmt = select(User).where(
            User.chat_id == chat_id,
            User.tg_user_id == tg_user_id,
        )
        user = await session.scalar(stmt)
        return user


async def create_user(chat_id, tg_user_id, username=None, nickname=None):
    async with session_maker() as session:
        user = User(
            chat_id=chat_id,
            tg_user_id=tg_user_id,
            username=username,
            nickname=nickname
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
