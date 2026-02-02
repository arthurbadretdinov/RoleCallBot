from aiogram import Router
from aiogram.types import Message
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(F.text.startswith("/"))
async def unknown_cmd(message: Message, session: AsyncSession):
    await message.answer(
        "❌ Команда не распознана.\n"
        "Пожалуйста, используйте /help для получения списка доступных команд.\n"
    )