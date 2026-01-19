from aiogram import BaseMiddleware

class GroupOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        
        if event.chat.type not in ("group", "supergroup"):
            return await event.answer(
                "⚠️ Команды работают только в группах!"
            )
        
        return await handler(event, data)
         