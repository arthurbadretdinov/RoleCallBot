from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.role_repo import get_role


async def ensure_role_unique(session: AsyncSession, chat_id: int, role_name: str) -> None:
    existing = await get_role(session, chat_id, role_name)
    
    if existing:
        raise ValueError("роль с таким именем уже существует")
    