from config import dp, bot
from aiogram.filters import Command
from databases import database
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import LabeledPrice
from bot.keyboard import keyboards

class Input(StatesGroup):
    count_star = State()
    count_max_star = State()
    count_max_gift = State()

@dp.message(Command('cancel'))
@dp.message(Command('start'))
@dp.message(Command('menu'))
async def start(message):
    check = await database.insert_data(message.from_user.id, message.from_user.username)
    if check:
        await message.answer('САЛО БРАТ. Это бот-скупщик подарков (нелегальный)')
        await message.answer('''
Профиль:

Звезд на аккаунте: 0      
        ''', reply_markup = keyboards.star_pay())
    else:
        info_user = await database.select_user(message.from_user.id)

        await message.answer(f'''
Профиль:

Звезд на аккаунте: {info_user.star_count}
Max звезд за 1 подарок: {info_user.max_limit}    
Max купится за 1 раз: {info_user.star_count}
                ''', reply_markup = keyboards.star_pay())

@dp.callback_query()
async def deposit(data, state):
    info = data.data
    if info == 'deposit':
        text = 'Сколько...'
        await state.set_state(Input.count_star)
    elif info == 'replace_maxstar':
        text = 'Введи максимальное количество звезд за 1 подарок'
        await state.set_state(Input.count_max_star)
    elif info == 'replace_maxgift':
        await state.set_state(Input.count_max_gift)
        text = 'Введи максимальное количество подарков, которые купятся, введи 0, если хочешь закупиться на всю котлету'
    await bot.send_message(
        data.from_user.id,
        text = text
    )
    await data.answer()

@dp.message(Input.count_max_star)
async def star_dep(message, state):
    if message.text.isdigit():
        await database.update_user(message.from_user.id, 'max_limit', int(message.text))
        await bot.send_message(message.from_user.id, text='💙 Изменено')
        await state.clear()

@dp.message(Input.count_max_gift)
async def star_dep(message, state):
    if message.text.isdigit():
        await database.update_user(message.from_user.id, 'count_gift', int(message.text))
        await bot.send_message(message.from_user.id, text='💙 Изменено')
        await state.clear()


@dp.message(Input.count_star)
async def star_dep(message, state):
    if message.text.isdigit():
        prices = [LabeledPrice(label="XTR", amount=int(message.text))]
        await bot.send_invoice(
            chat_id = message.from_user.id,
            title = f'💜 Пополнение баланса',
            description = '⭐ После успешной оплаты кнопка внизу поменятся на чек. Для отмены нажми /cancel',
            payload = 'test',
            currency = 'XTR',
            prices = prices,
            start_parameter='vip1'
        )
        await state.clear()

@dp.pre_checkout_query()
async def payment(query):
    info_old = await database.select_user(query.from_user.id)
    await database.update_user(user_id = query.from_user.id, column = 'star_count', value= info_old.star_count + query.total_amount)
    await query.answer(ok=True, text= '💙 Баланс пополнен 💜')
    await bot.send_message(query.from_user.id, text = '💙 Баланс пополнен 💜')