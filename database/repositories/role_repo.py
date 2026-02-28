from sqlalchemy import select, delete

from database.models.role import Role


async def get_role(session, chat_id, role_name):
    stmt = select(Role).where(
        Role.chat_id == chat_id, 
        Role.name == role_name
    )
    role = await session.scalar(stmt)
    return role


async def get_all_role_names(session, chat_id):
    stmt = select(Role.name).where(
        Role.chat_id == chat_id
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_existing_role_names(session, chat_id, names):
    if not names:
        return []
    
    stmt = select(Role.name).where(
        Role.chat_id == chat_id,
        Role.name.in_(names)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_roles(session, chat_id, role_names): 
    roles = [Role(chat_id=chat_id, name=name) for name in role_names]
    session.add_all(roles)
  
    
async def delete_roles(session, chat_id, role_names): 
    stmt = delete(Role).where(
        Role.chat_id == chat_id,
        Role.name.in_(role_names)
    )
    await session.execute(stmt)
    