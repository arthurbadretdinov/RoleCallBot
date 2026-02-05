from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.user_repo import delete_user, get_user, create_user, update_user_active, update_user_nickname
from utils.command_args import validate_command_args

router = Router()


async def setactive_status(message: Message, session: AsyncSession, is_active: bool):
    args = await validate_command_args(message, max_args=1)
    if args is None:
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    chat_id = chat.id
    tg_user_id = message.from_user.id
    
    user = await update_user_active(session, chat_id, tg_user_id, is_active)
    if not user:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")
        return
    
    status_text = "активный" if is_active else "неактивный"
    await message.answer(f"✅ Вы помечены как {status_text} участник.")


@router.message(Command("registerme"))
async def registerme_cmd(message: Message, session: AsyncSession):
    args = await validate_command_args(message, max_args=2)
    if args is None:
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    username = message.from_user.username
    nickname = args[1] if len(args) == 2 else None
    
    user = await get_user(session, chat_id, tg_user_id)
    if user:
        await message.answer("❌ Вы уже зарегистрированы.")
        return
    
    user = await create_user(session, chat_id, tg_user_id, username=username, nickname=nickname)
    await message.answer("✅ Вы успешно зарегистрированы!")
    

@router.message(Command("unregisterme"))
async def unregisterme_cmd(message: Message, session: AsyncSession):
    args = await validate_command_args(message, max_args=1)
    if args is None:
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    
    deleted = await delete_user(session, chat_id, tg_user_id)
    if not deleted:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")
        return
    
    await message.answer("✅ Вы успешно удалены из базы данных.")


@router.message(Command("setnicknameme"))
async def setnicknameme_cmd(message: Message, session: AsyncSession):
    args = await validate_command_args(message, max_args=2)
    if args is None:
        return
    elif len(args) == 1:
        await message.answer("❌ Ошибка: никнейм не указан.") 
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    chat_id = chat.id
    tg_user_id = message.from_user.id
    nickname = args[1]
    
    user = await update_user_nickname(session, chat_id, tg_user_id, nickname)
    if not user:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")
        return
    
    await message.answer(f"✅ Ваш никнейм изменён на: {nickname}")
    
    
@router.message(Command("setactive"))
async def setactive_cmd(message: Message, session: AsyncSession):
    await setactive_status(message, session, is_active=True)
  
    
@router.message(Command("setinactive"))
async def setinactive_cmd(message: Message, session: AsyncSession):
    await setactive_status(message, session, is_active=False)