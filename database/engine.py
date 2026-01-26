from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import BaseModel


engine = create_async_engine(
    url="sqlite+aiosqlite:///role_call_bot.db",
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_model():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)