import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import help, admin, user, profile, roles, call, fallback
from middlewares.is_group import GroupOnlyMiddleware
from database.engine import init_model


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.middleware(GroupOnlyMiddleware())
    
    dp.include_routers(
        help.router, 
        admin.router, 
        user.router, 
        profile.router, 
        roles.router, 
        call.router,
        fallback.router
    )
    
    await init_model()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен вручную.")