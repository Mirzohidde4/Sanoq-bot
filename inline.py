from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


start = InlineKeyboardBuilder()
start.add(InlineKeyboardButton(text="✅ Qollanma", callback_data="start_qollanma"))
start.add(InlineKeyboardButton(text="🔎 Buyruqlar", callback_data="start_buyruqlar"))


menu = InlineKeyboardBuilder()
menu.add(InlineKeyboardButton(text='➕ Guruhga admin qilish', url='https://t.me/sanoq_uz_bot?startgroup=new'))
menu.add(InlineKeyboardButton(text='🔝 Asosiy menyu', callback_data='canal_main'))
menu.adjust(1)