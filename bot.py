import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8378672447:**************************"  # BU YERGA TOKENINGIZ
GROUP_ID = -1003325165006

bot = Bot(token="8378672447:AAE5O3v6kUY-146MC-cGkpAaPjeWeK0kufw")
dp = Dispatcher(storage=MemoryStorage())


# FORM HOLATI
class Form(StatesGroup):
    fio = State()
    phone = State()
    video = State()


# /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Salom! F.I.O kiriting:")
    await state.set_state(Form.fio)


# FIO
@dp.message(Form.fio)
async def get_fio(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Form.phone)


# PHONE
@dp.message(Form.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Endi videoni yuboring:")
    await state.set_state(Form.video)


# VIDEO
@dp.message(Form.video, F.video)
async def get_video(message: types.Message, state: FSMContext):
    global GROUP_ID

    data = await state.get_data()
    fio = data["fio"]
    phone = data["phone"]
    file_id = message.video.file_id

    caption = f"📌 Yangi ishtirokchi!\n👤 FIO: {fio}\n📞 Telefon: {phone}"

    if GROUP_ID is None:
        await message.answer("⚠️ Guruh chat ID hali o'rnatilmagan!")
        return

    await bot.send_video(chat_id=GROUP_ID, video=file_id, caption=caption)
    await message.answer("Video qabul qilindi! Rahmat!")

    await state.clear()


# ❗ CHAT ID olish buyrug'i
@dp.message(Command("chatid"))
async def chat_id_cmd(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"Chat ID: `{chat_id}`", parse_mode="Markdown")


# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
