from sqlalchemy import select

from database.models.user import User
            

async def get_user(session, chat_id, tg_user_id):
    stmt = select(User).where(
        User.chat_id == chat_id,
        User.tg_user_id == tg_user_id,
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
    await session.refresh(user)
    return user
    

async def update_user_nickname(session, chat_id, tg_user_id, new_nickname):
    user = await get_user(session, chat_id, tg_user_id)
    
    if not user:
        return None
    
    user.nickname = new_nickname
    await session.commit()
    return user
