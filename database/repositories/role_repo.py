from sqlalchemy import select

from database.models.role import Role


async def get_role(session, chat_id, role_name):
    stmt = select(Role).where(
        Role.chat_id == chat_id, 
        Role.name == role_name
    )
    role = await session.scalar(stmt)
    return role


async def create_role(session, chat_id, role_name): 
    role = Role(
        chat_id=chat_id, 
        name=role_name
    )
    session.add(role)
    await session.commit()