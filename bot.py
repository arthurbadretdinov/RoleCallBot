import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import help, call, fallback
from handlers.admin import roles as admin_roles, users as admin_users
from handlers.roles import self as roles_self, info as roles_info
from handlers.user import others as user_others, self_info as user_self_info, self_manage as user_self_manage
from middlewares.is_group import GroupOnlyMiddleware
from database.db import init_model


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.message.middleware(GroupOnlyMiddleware())
    
    dp.include_routers(
        help.router, 
        admin_roles.router, 
        admin_users.router,
        user_self_manage.router,
        user_self_info.router,
        user_others.router,
        roles_self.router,
        roles_info.router,
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