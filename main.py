import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, FSInputFile, ChatPermissions
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from dt_base import Add_db, Read_db


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user.full_name
    await message.answer(text=f"Assalomu alaykum {html.bold(user)}")


@dp.message(F.text == 'salom', F.chat.type == "supergroup")
async def group(message: Message):
    await message.reply(text="Salom")


@dp.message(F.chat.type == "supergroup", F.new_chat_members)
async def ner_member(message: Message):
    new_members = message.new_chat_members  # Yangi a'zolar ro'yxati
    inviter = message.from_user  # Yangi a'zolarni qo'shgan foydalanuvchi
    chat_id = message.chat.id

    for member in new_members:
        if member.id == inviter.id:
            await message.answer(text=f"Assalomu alaykum {member.full_name}")
        else:
            Add_db(chat_id=chat_id, user_id=inviter.id, fullname=inviter.full_name, soni=1)

    natija = "Natijalar :"
    for user in Read_db():
        if user[0] == chat_id:  
            natija += f"\n{user[2]} - {html.bold(user[3])} ta"
    await message.answer(text=natija)            
    await message.delete()


@dp.message(F.chat.type == "supergroup", F.left_chat_member)
async def ner_member(message: Message):
    await message.answer(text=f"Xayr {message.left_chat_member.full_name}")
    await message.delete()


@dp.message(F.chat.type == "supergroup", and_f(F.text == "yozma", F.reply_to_message))
async def yozma(message: Message):
    user_id = message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=False)
    await message.chat.restrict(user_id=user_id, permissions=permission)
    await message.answer(text=f"Siz endi yoza olmaysiz\n{message.reply_to_message.from_user.full_name}")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "yoz", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=True)
    await message.chat.restrict(user_id=user_id, permissions=permission)
    await message.answer(text=f"Siz endi yoza olasiz\n{message.reply_to_message.from_user.full_name}")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "ban", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_sender_chat(user_id)
    await message.answer(text=f"Siz endi guruhga qo'shila olmaysiz\n{message.reply_to_message.from_user.full_name}")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "unban", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.unban_sender_chat(user_id)
    await message.answer(text=f"Siz endi guruhga qo'shila olasiz\n{message.reply_to_message.from_user.full_name}")


@dp.message(F.text)
async def echo(message: Message):
    await message.answer(text=f"{message.text}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")   