from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.markdown import hbold
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram import F
import asyncio

# 🔐 Токен и ID группы
TOKEN = "8207794176:AAHqf1pphiDg0mkYDJ2_hYtWxTJY1R53bNM"
GROUP_CHAT_ID = -1002834809117

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Состояния для формы заявки
user_data = {}

# Главное меню
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧾 О нас")],
        [KeyboardButton(text="✉️ Оставить заявку")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {hbold(message.from_user.first_name)}! 👋\nВыберите пункт меню ниже 👇",
        reply_markup=menu_keyboard
    )

@dp.message(F.text == "🧾 О нас")
async def about_handler(message: Message):
    await message.answer(
        "Компания <b>Proflon</b> специализируется на профессиональном "
        "нанесении фторполимерных покрытий, обеспечивая защиту оборудования "
        "от агрессивных сред и износа. Мы также предоставляем консультации "
        "по выбору и применению покрытий под ваши задачи."
    )

@dp.message(F.text == "✉️ Оставить заявку")
async def start_application(message: Message):
    user_data[message.from_user.id] = {}
    await message.answer("Введите ваше <b>имя</b>:")

@dp.message(lambda m: m.from_user.id in user_data and "name" not in user_data[m.from_user.id])
async def get_name(message: Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Введите ваш <b>телефон</b>:")

@dp.message(lambda m: m.from_user.id in user_data and "phone" not in user_data[m.from_user.id])
async def get_phone(message: Message):
    user_data[message.from_user.id]["phone"] = message.text
    await message.answer("Введите ваш <b>email</b>:")

@dp.message(lambda m: m.from_user.id in user_data and "email" not in user_data[m.from_user.id])
async def get_email(message: Message):
    user_data[message.from_user.id]["email"] = message.text
    await message.answer("Кратко опишите <b>задачу</b>:")

@dp.message(lambda m: m.from_user.id in user_data and "task" not in user_data[m.from_user.id])
async def get_task(message: Message):
    user_id = message.from_user.id
    user_data[user_id]["task"] = message.text

    data = user_data.pop(user_id)  # очищаем после заявки

    # Формируем текст заявки
    text = (
        "Спасибо! Заявка получена ✅\n\n"
        f"<b>Имя:</b> {data['name']}\n"
        f"<b>Телефон:</b> {data['phone']}\n"
        f"<b>Email:</b> {data['email']}\n"
        f"<b>Задача:</b> {data['task']}\n\n"
        "С вами свяжутся в ближайшее время!"
    )

    # Ответ пользователю
    await message.answer(text)

    # Уведомление в группу
    await bot.send_message(GROUP_CHAT_ID, f"📥 <b>Новая заявка:</b>\n\n{text}")

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
