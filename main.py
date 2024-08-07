import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, FSInputFile, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, and_f
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from config import TOKEN
from dt_base import Add_db, Read_db, Update_Soni
from inline import start, menu


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def smd_start(message: Message):
    await message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=f40b8e1a8e992e4f073a8cef5964ff7b9c4b359c-9065820-images-thumbs&n=13',
        caption=html.bold("Assalomu alaykum xush kelibsiz."),
        reply_markup=start.as_markup()
    )


@dp.callback_query(F.data.startswith('start_'))
async def btn(call: CallbackQuery):
    await call.message.delete()
    action = call.data.split('_')
    word = action[1]

    if word == 'qollanma':
         await call.message.answer(
            text=f"""
                <b>⚜️ Shartlar :
1. Botni (@sanoq_uz_bot) guruhingizga qo'shing.
    
2. Botni guruhingizda administratorlar ro'yxatiga qo'shib qo'ying.</b>
            """, reply_markup=menu.as_markup()
        )

    elif word == 'buyruqlar':
        await call.message.answer(text=f'''
            {html.bold('Guruhlarda botdan foydalanish uchun buyruqlar\n(1-dan tashqari barcha buyruqlar reply qilib yozilsa ishlaydi) :')}
1 . {html.bold('/natijalar')} - guruhga kim qancha odam qo'shganini aniqlash (bot ishga tushgan vaqtdan boshlab).
2.  {html.bold('yozma')} - guruhda foydalanuvchiga yozishni taqiqlab qo'yish.
3. {html.bold('yoz')} - yuqoridagi foydalanuvchuga yozishga ruxsat berish.
4.  {html.bold('ban')} - guruhda foydalanuvchini chiqarib yuborish va qora ro'yhatga qo'shish.
5. {html.bold('unban')} - yuqoridagi foydalanuvchini qora royhatdan chiqarish va guruhga qo'shilishga ruxsat berish.    
    ''',
    reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔝 Asosiy menyu', callback_data='canal_main')]
        ]
    )
    ) 
        

@dp.callback_query(F.data.startswith('canal'))
async def back(call: CallbackQuery):
    await call.message.delete()
    action = call.data.split('_')
    word = action[1]

    if word == 'main':
            await call.message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=f40b8e1a8e992e4f073a8cef5964ff7b9c4b359c-9065820-images-thumbs&n=13',
        caption=html.bold("🏠 Asosiy menyuga qaytdingiz."),
        reply_markup=start.as_markup()
    )


@dp.message(F.chat.type == "supergroup", F.new_chat_members)
async def nev_member(message: Message):
    new_members = message.new_chat_members  # Yangi a'zolar ro'yxati
    inviter = message.from_user  # Yangi a'zolarni qo'shgan foydalanuvchi
    chat_id = message.chat.id

    for member in new_members:
        if member.id == inviter.id:
            await message.answer(text=f"Assalomu alaykum {html.bold(member.full_name)}")

        elif member.is_bot:
            continue

        else:
            for user in Read_db():
                if (user[0] == chat_id) and (user[1] == inviter.id):
                    soni = user[3] + 1
                    Update_Soni(soni=soni, chat_id=chat_id, user_id=inviter.id)
                    break
            # else: 
            Add_db(chat_id=chat_id, user_id=inviter.id, fullname=inviter.full_name, soni=1)            
    await message.delete()


@dp.message(Command("natijalar"), F.chat.type == "supergroup")
async def natijalar(message: Message):
    chat_id = message.chat.id

    chat_list = []
    for user in Read_db():
        if user[0] == chat_id:
            chat_list.append(user)  

    sorted_tuple_list = sorted(chat_list, key=lambda x: x[3], reverse=True)
    wag = 1
    natija = "<b>Natijalar :</b>"
    for tupl in sorted_tuple_list:
        natija += f"\n{wag}. {html.bold(tupl[2])} - {html.bold(tupl[3])} ta"  
        wag += 1      
    await message.reply(text=natija)    


@dp.message(F.chat.type == "supergroup", F.left_chat_member)
async def ner_member(message: Message):
    # await message.answer(text=f"Xayr {message.left_chat_member.full_name}")
    await message.delete()


@dp.message(F.chat.type == "supergroup", and_f(F.text == "yozma", F.reply_to_message))
async def yozma(message: Message):
    user_id = message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=False)
    await message.chat.restrict(user_id=user_id, permissions=permission)
    await message.answer(text=f"{message.reply_to_message.from_user.full_name}\nSiz endi yoza olmaysiz.")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "yoz", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=True)
    await message.chat.restrict(user_id=user_id, permissions=permission)
    await message.answer(text=f"{message.reply_to_message.from_user.full_name}\nSiz endi yoza olasiz.")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "ban", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_sender_chat(user_id)
    await message.answer(text=f"{message.reply_to_message.from_user.full_name}\nSiz endi guruhga qo'shila olmaysiz.")


@dp.message(F.chat.type == "supergroup", and_f(F.text == "unban", F.reply_to_message))
async def yoz(message: Message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.unban_sender_chat(user_id)
    await message.answer(text=f"{message.reply_to_message.from_user.full_name}\nSiz endi guruhga qo'shila olasiz.")


# @dp.message(F.text)
# async def echo(message: Message):
#     await message.answer(text="Botni qayta ishga tushirish uchun /start ni bosing.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")   