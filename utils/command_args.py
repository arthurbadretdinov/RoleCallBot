from aiogram.types import Message

async def validate_command_args(message: Message, max_args: int): 
    args = message.text.split()
    
    if len(args) > max_args: 
        await message.answer("❌ Ошибка: слишком много аргументов") 
        return None
    
    return args