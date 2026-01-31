from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.user_repo import get_user, create_user

router = Router()


@router.message(Command("registerme"))
async def registerme_cmd(message: Message):
    args = message.text.split()
    if len(args) > 2:
        await message.answer("❌ Ошибка: слишком много аргументов. Используйте: /registerme [никнейм - необязательно].") 
        return
    
    chat = await get_or_create_chat(message.chat.id)
    
    chat_id = chat.id
    tg_user_id = message.from_user.id
    username = message.from_user.username
    nickname = args[1] if len(args) == 2 else None
    
    user = await get_user(chat_id, tg_user_id)
    if user:
        await message.answer("❌ Вы уже зарегистрированы.")
        return
    
    user = await create_user(chat_id, tg_user_id, username=username, nickname=nickname)
    await message.answer("✅ Вы успешно зарегистрированы!")
    

@router.message(Command("unregisterme"))
async def unregisterme_cmd(message: Message):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
    

@router.message(Command("setnicknameme"))
async def setnicknameme_cmd(message: Message):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )

    
@router.message(Command("setactive"))
async def setactive_cmd(message: Message):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
  
    
@router.message(Command("setinactive"))
async def setinactive_cmd(message: Message):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )