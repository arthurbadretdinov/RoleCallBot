import shlex
from aiogram.filters import CommandObject

async def validate_command_args(
    command: CommandObject, 
    min_args: int = 0, 
    max_args: int | None = None
) -> list[str]: 
    try:
        args = shlex.split(command.args or "")
    except ValueError:
        raise ValueError(
            "неверный формат команды. Используйте кавычки для аргументов с пробелами."
        )

    if len(args) < min_args:
        raise ValueError(
            f"недостаточно аргументов (минимум {min_args})."
        )
    
    if max_args is not None and len(args) > max_args:
        raise ValueError(
            f"слишком много аргументов (максимум {max_args})."
        )
    
    return args