import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import help, admin, user, profile, roles, call


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_routers(
        help.router, 
        admin.router, 
        user.router, 
        profile.router, 
        roles.router, 
        call.router
    )
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен вручную.")