from email.mime import message
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.user_repo import get_user

router = Router()


@router.message(Command("myinfo"))
async def myinfo_cmd(message: Message, session: AsyncSession):
    args = message.text.split()
    if len(args) > 1:
        await message.answer("❌ Ошибка: слишком много аргументов") 
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    
    user = await get_user(session, chat_id, tg_user_id)
    
    if user:
        await message.answer(
            f"ℹ️ Твоя информация:\n"
            f"Никнейм: {user.nickname if user.nickname else 'Не указан'}\n"
            f"Статус: {'Активный' if user.is_active else 'Неактивный'}\n"
        )
    else:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")
    
@router.message(Command("mystatus"))
async def mystatus_cmd(message: Message, session: AsyncSession):
    args = message.text.split()
    if len(args) > 1:
        await message.answer("❌ Ошибка: слишком много аргументов") 
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    
    user = await get_user(session, chat_id, tg_user_id)
    
    if user:
        await message.answer(
            f"ℹ️ Ваш статус: {'Активный' if user.is_active else 'Неактивный'}\n"
        )
    else:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")


    
@router.message(Command("myroles"))
async def myroles_cmd(message: Message, session: AsyncSession):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
    
@router.message(Command("mynickname"))
async def mynickname_cmd(message: Message, session: AsyncSession):
    args = message.text.split()
    if len(args) > 1:
        await message.answer("❌ Ошибка: слишком много аргументов") 
        return
    
    chat = await get_or_create_chat(session, message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    
    user = await get_user(session, chat_id, tg_user_id)
    
    if user:
        await message.answer(
            f"ℹ️ Ваш никнейм: {user.nickname if user.nickname else 'Не указан'}\n"
        )
    else:
        await message.answer("❌ Ошибка. Вы не зарегистрированы. Сначала используйте /registerme.")