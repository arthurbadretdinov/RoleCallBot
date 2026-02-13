import shlex
from aiogram.types import Message
from aiogram.filters import CommandObject

async def validate_command_args(
    message: Message, 
    command: CommandObject, 
    min_args: int = 0, 
    max_args: int | None = None
) -> list[str] | None: 
    try:
        args = shlex.split(command.args or "")
    except ValueError:
        await message.answer("❌ Ошибка: неверный формат команды. Используйте кавычки для аргументов с пробелами.")
        return None
    
    if len(args) < min_args:
        await message.answer(f"❌ Ошибка: недостаточно аргументов (минимум {min_args}).")
        return None
    
    if max_args is not None and len(args) > max_args: 
        await message.answer(f"❌ Ошибка: слишком много аргументов (максимум {max_args}).") 
        return None
    
    return args