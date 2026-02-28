from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.chat_repo import get_or_create_chat
from database.repositories.role_repo import get_all_role_names
from utils.validator import validate_command_args

router = Router()


@router.message(Command("roleslist"))
async def roleslist_cmd(
    message: Message, 
    command: CommandObject, 
    session: AsyncSession
):
    chat = await get_or_create_chat(session, message.chat.id)
    chat_id = chat.id
    
    try:
        validate_command_args(command.args, max_args=0)
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}.")
        return
    
    role_names = await get_all_role_names(session, chat_id)
    if role_names:
        await message.answer(
            "Существующие роли:\n" + "\n".join(f"{i+1}. {name}" for i, name in enumerate(role_names))
            )
    else:
        await message.answer("❌ Роли не созданы.")


@router.message(Command("roleusers"))
async def roleusers_cmd(message: Message):
    command = message.text.split()[0] 
    args = message.text.split(maxsplit=1)
    args_text = args[1] if len(args) > 1 else ""
    
    await message.answer(
        f"Команда: {command}\n"
        f"Аргументы: {args_text}\n"
        "Команда на данный момент не реализована."
    )