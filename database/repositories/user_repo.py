from sqlalchemy import select

from database.models.user import User
            

async def get_user_by_tg_id(session, chat_id, tg_user_id):
    stmt = select(User).where(
        User.chat_id == chat_id,
        User.tg_user_id == tg_user_id,
    )
    user = await session.scalar(stmt)
    return user


async def get_user_by_nickname(session, chat_id, nickname):
    stmt = select(User).where(
        User.chat_id == chat_id,
        User.nickname == nickname,
    )
    user = await session.scalar(stmt)
    return user


async def get_user_by_username(session, chat_id, username):
    stmt = select(User).where(
        User.chat_id == chat_id,
        User.username == username,
    )
    user = await session.scalar(stmt)
    return user


async def create_user(session, chat_id, tg_user_id, username=None, nickname=None):
    user = User(
        chat_id=chat_id,
        tg_user_id=tg_user_id,
        username=username,
        nickname=nickname
    )
    session.add(user)
    await session.commit()


async def delete_user(session, user):
    await session.delete(user)
    await session.commit()


async def update_user_nickname(session, user, new_nickname):
    user.nickname = new_nickname
    await session.commit()


async def update_user_active(session, user, is_active):
    user.is_active = is_active
    await session.commit()
