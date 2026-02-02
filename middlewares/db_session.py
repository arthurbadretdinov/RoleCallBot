from aiogram import BaseMiddleware
from database.db import session_maker

class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with session_maker() as session:
            data['session'] = session
            return await handler(event, data)