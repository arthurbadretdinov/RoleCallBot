from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.user_repo import delete_user, create_user, update_user_active, update_user_nickname
from utils.validator import validate_command_args, validate_length
from utils.current_user import get_current_user_with_chat_ids, require_current_user

router = Router()


async def setactive_status(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession, 
    is_active: bool
):
    try:
        await validate_command_args(command, max_args=0)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return
    
    is_status = "активный" if is_active else "неактивный"
    await update_user_active(session, user, is_active)
    await message.answer(f"✅ Вы помечены как {is_status} участник.")


@router.message(Command("registerme"))
async def registerme_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    try:
        args = await validate_command_args(command, max_args=1)
        nickname = validate_length(args[0], 64) if args else None 
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
    user, chat_id, tg_user_id = await get_current_user_with_chat_ids(session, message)
    if user:
        await message.answer("❌ Вы уже зарегистрированы.")
        return
    
    username = message.from_user.username
    
    await create_user(session, chat_id, tg_user_id, username=username, nickname=nickname)
    await message.answer("✅ Вы успешно зарегистрированы!")
    

@router.message(Command("unregisterme"))
async def unregisterme_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    try:
        await validate_command_args(command, max_args=0)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return
    
    await delete_user(session, user)
    await message.answer("✅ Вы успешно удалены из базы данных.")


@router.message(Command("setnicknameme"))
async def setnicknameme_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    try:
        args = await validate_command_args(command, min_args=1, max_args=1)
        nickname = validate_length(args[0], 64)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return
    
    await update_user_nickname(session, user, nickname)
    await message.answer(f"✅ Ваш никнейм изменён на: {nickname}")
    
    
@router.message(Command("setactive"))
async def setactive_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    await setactive_status(message, command, session, is_active=True)
  
    
@router.message(Command("setinactive"))
async def setinactive_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    await setactive_status(message, command, session, is_active=False)