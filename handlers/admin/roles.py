from concurrent.futures import wait

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.role_repo import create_role
from database.services.role_service import ensure_role_unique
from middlewares.is_admin import AdminOnlyMiddleware
from utils.validator import validate_command_args, validate_length, validate_name

router = Router()
router.message.middleware(AdminOnlyMiddleware())


@router.message(Command("createrole"))
async def createrole_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    chat = await get_or_create_chat(session, message.chat.id)
    chat_id = chat.id
    
    try:
        args = validate_command_args(command.args, min_args=1)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}.")
        return
        
    args = list(set(args))
    
    messages = []
        
    for role_name in args:
        try:
            validate_name(role_name)
            validate_length(role_name, 64)
            await ensure_role_unique(session, chat_id, role_name)
            
            await create_role(session, chat_id, role_name)
            messages.append(f"✅ {role_name} - cоздана.")
            
        except ValueError as e:
            messages.append(f"❌ {role_name} - ошибка: {e}.")
        
        except IntegrityError:
            await session.rollback()
            messages.append(f"❌ {role_name} - ошибка: роль с таким именем уже существует.")
        
    await message.answer("\n".join(messages))
        
        

        
    
    
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