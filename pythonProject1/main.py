from databases.connect import init_db
import asyncio
from config import dp, bot
from bot import handlers, gift_send

from aiogram import Router

router = Router()

async def on_startup():
    asyncio.create_task(gift_send.sender())

def main():
    dp.include_router(router)

    dp.startup.register(on_startup)

    dp.run_polling(bot)

if __name__ == "__main__":
    main()