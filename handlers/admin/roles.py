from concurrent.futures import wait

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.role_repo import create_roles, get_existing_role_names
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
        
    args = list(dict.fromkeys(args))
    
    messages = []
    existing_names = await get_existing_role_names(session, chat_id, args)
    roles_to_add = []
        
    for role_name in args:
        try:
            validate_name(role_name)
            validate_length(role_name, 64)
            
            if role_name in existing_names:
                raise ValueError("роль с таким именем уже существует.")
            
            roles_to_add.append(role_name)
            messages.append(f"✅ {role_name} - cоздана.")  
        except ValueError as e:
            messages.append(f"❌ {role_name} - ошибка: {e}.")
        
    try:
        if roles_to_add:
            create_roles(session, chat_id, roles_to_add)
            await session.commit()
    except Exception:
        await session.rollback()
        await message.answer(f"❌ Ошибка: не удалось создать роли. Попробуйте еще раз.")
        return
    
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