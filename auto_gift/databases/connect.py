from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base
DATABASE_URL = "sqlite+aiosqlite:///databases/db.sqlite3"

async_engine = create_async_engine(DATABASE_URL, echo = False)

async_session = async_sessionmaker(async_engine)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)