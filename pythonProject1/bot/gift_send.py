from aiogram import types
from config import bot
from databases import database
import asyncio
default_sticker = [
    '5170145012310081615',
    '5170233102089322756',
    '5170250947678437525',
    '5168103777563050263',
    '5170144170496491616',
    '5170314324215857265',
    '5170564780938756245',
    '5168043875654172773',
    '5170690322832818290',
    '5170521118301225164',
    '6028601630662853006'

]
async def sender_gift(gift_id, user_to):
    await bot.send_gift(gift_id, user_to)

async def sender():
    while True:
        text = await bot.get_available_gifts()
        for x in text.gifts:
            if x.id not in default_sticker:
                default_sticker.append(x.id)
                users = await database.select_user(much=True)
                for user in users:
                    await bot.send_message(user.user_id, 'Вышли новые ПОДАРКИ!!!!!!!!!!!')
                    if user.max_limit >= x.star_count:
                        for y in range(x.count_gift):
                            await sender_gift(x.id, user.user_id)
                            await bot.send_message(user.user_id, f'Купил {x.star_count}⭐')
                    else:
                        await bot.send_message(user.user_id, f'Пропуск. Высока цена: {x.star_count}⭐')
        await asyncio.sleep(5)

