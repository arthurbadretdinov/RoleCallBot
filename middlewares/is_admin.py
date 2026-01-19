from aiogram import BaseMiddleware
from aiogram.enums import ChatMemberStatus

class AdminOnlyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        user = await event.bot.get_chat_member(
            event.chat.id, 
            event.from_user.id
        )
        
        if user.status not in (
            ChatMemberStatus.ADMINISTRATOR, 
            ChatMemberStatus.CREATOR
        ):
            return await event.answer(
                "⚠️ Команды работают только для администраторов!"
            )

        return await handler(event, data)