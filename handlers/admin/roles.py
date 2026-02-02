from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares.is_admin import AdminOnlyMiddleware

router = Router()
router.message.middleware(AdminOnlyMiddleware())


@router.message(Command("createrole"))
async def createrole_cmd(message: Message, session: AsyncSession):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
    
    
@router.message(Command("deleterole"))
async def deleterole_cmd(message: Message, session: AsyncSession):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )

    
@router.message(Command("addroleuser"))
async def addroleuser_cmd(message: Message, session: AsyncSession):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
  
    
@router.message(Command("removeroleuser"))
async def removeroleuser_cmd(message: Message, session: AsyncSession):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )