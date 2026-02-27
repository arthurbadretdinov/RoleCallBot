from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.user_repo import delete_user, create_user, update_user_active, update_user_nickname
from database.services.user_service import ensure_nickname_unique, get_current_chat_and_user, require_current_chat_and_user
from utils.validator import validate_command_args, validate_length

router = Router()


async def setactive_status(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession, 
    is_active: bool
):
    try:
        _, user = await require_current_chat_and_user(session, message)
        validate_command_args(command.args, max_args=0)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
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
        chat, user = await get_current_chat_and_user(session, message)
        if user:
            raise ValueError("вы уже зарегистрированы.")
        
        args = validate_command_args(command.args, max_args=1)
        
        chat_id = chat.id
        tg_user_id = message.from_user.id
        username = message.from_user.username
        nickname = validate_length(args[0], 64) if args else None
        await ensure_nickname_unique(session, chat_id, nickname) 

        try:
            await create_user(session, chat_id, tg_user_id, username=username, nickname=nickname)
        except IntegrityError:
            await session.rollback()
            raise ValueError("этот никнейм уже занят другим пользователем.")
    
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
    await message.answer("✅ Вы успешно зарегистрированы!")
    

@router.message(Command("unregisterme"))
async def unregisterme_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    try:
        _, user = await require_current_chat_and_user(session, message)
        validate_command_args(command.args, max_args=0)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
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
        chat, user = await require_current_chat_and_user(session, message)
        
        args = validate_command_args(command.args, min_args=1, max_args=1)
        nickname = validate_length(args[0], 64)
        await ensure_nickname_unique(session, chat.id, nickname)
        
        try:
            await update_user_nickname(session, user, nickname)
        except IntegrityError:
            await session.rollback()
            raise ValueError("этот никнейм уже занят другим пользователем.")
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")
        return
    
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