import re
import shlex


def validate_command_args(
    command: str,   
    min_args: int = 0, 
    max_args: int | None = None
) -> list[str]: 
    try:
        args = shlex.split(command or "")
    except ValueError:
        raise ValueError(
            "неверный формат команды. Используйте кавычки для аргументов с пробелами"
        )

    if len(args) < min_args:
        raise ValueError(
            f"недостаточно аргументов (минимум {min_args})"
        )
    
    if max_args is not None and len(args) > max_args:
        raise ValueError(
            f"слишком много аргументов (максимум {max_args})"
        )
    
    return args


def validate_length(
    value: str,
    max_length: int = 64
) -> str:
    if not value: 
        raise ValueError("строка не может быть пустой")
    
    if len(value) > max_length:
        raise ValueError(f"максимальная длина - {max_length} символов")
    
    return value


def validate_name(
    name: str
) -> str:
    if name != name.strip():
        raise ValueError(f"имя не должно содержать пробелы в начале или конце")
    
    if re.search(r"[\n\t\r]", name):
        raise ValueError(f"имя не должно содержать невидимые символы (табуляции, переводы строки)")
    
    if re.search(r"\s{2,}", name):
        raise ValueError(f"имя не должно содержать несколько пробелов подряд")
    
    if not re.fullmatch(r"[A-Za-zА-Яа-яЁё0-9 _-]+", name):
        raise ValueError(
            f"имя содержит недопустимые символы. "
            "Используйте только буквы, цифры, пробел, '-' и '_'"
        )  
    
    return name