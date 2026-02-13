from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from utils.command_args import validate_command_args
from utils.current_user import require_current_user

router = Router()


@router.message(Command("myinfo"))
async def myinfo_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    args = await validate_command_args(message, command, max_args=0)
    if args is None:
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return

    nickname = user.nickname or "Не указан"
    status = "Активный" if user.is_active else "Неактивный"

    await message.answer(
        f"ℹ️ Твоя информация:\n"
        f"Никнейм: {nickname}\n"
        f"Статус: {status}\n"
    )
   
 
@router.message(Command("mystatus"))
async def mystatus_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    args = await validate_command_args(message, command, max_args=0)
    if args is None:
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return
    
    status = "Активный" if user.is_active else "Неактивный"

    await message.answer(
        f"ℹ️ Ваш статус: {status}\n"
    )


@router.message(Command("myroles"))
async def myroles_cmd(
    message: Message,  
    session: AsyncSession
):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )
    

@router.message(Command("mynickname"))
async def mynickname_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    args = await validate_command_args(message, command, max_args=0)
    if args is None:
        return
    
    user = await require_current_user(session, message)
    if user is None:
        return
    
    nickname = user.nickname or "Не указан"
    
    await message.answer(
        f"ℹ️ Ваш никнейм: {nickname}\n"
    )