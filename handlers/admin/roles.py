from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.role_repo import create_role, get_role
from middlewares.is_admin import AdminOnlyMiddleware
from utils.command_args import validate_command_args

router = Router()
router.message.middleware(AdminOnlyMiddleware())


@router.message(Command("createrole"))
async def createrole_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    args = await validate_command_args(message, command, min_args=1, max_args=1)
    if args is None:
        return
    
    chat = await  get_or_create_chat(session, message.chat.id)
    role = await get_role(session, chat.id, args[0])
    if role:
        await message.answer("❌ Роль с таким именем уже существует.")
        return
    
    chat_id = chat.id
    role_name = args[0]
    
    await create_role(session, chat_id, role_name)
    await message.answer(f"✅ Роль '{role_name}' успешно создана.")
    
    
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