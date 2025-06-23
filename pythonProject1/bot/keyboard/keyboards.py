from aiogram.utils.keyboard import InlineKeyboardBuilder
def star_pay():
    builder = InlineKeyboardBuilder()
    builder.button(text=f'Пополнить баланс', callback_data='deposit')
    builder.button(text=f'Изменить max кол-во звезд за подарок', callback_data='replace_maxstar')
    builder.button(text=f'Изменить max кол-во подарков для покупки', callback_data='replace_maxgift')
    builder.adjust(1)
    return builder.as_markup()