import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== НАСТРОЙКИ =====
API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ===== /start =====
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🚀 Начать тест", callback_data="start_test"))

    await message.answer(
        "Привет 👋\n\nЭто тестовый бот.\nНажми кнопку ниже 👇",
        reply_markup=kb
    )

# ===== КНОПКА =====
@dp.callback_query_handler(lambda c: c.data == "start_test")
async def start_test(call: types.CallbackQuery):
    await call.message.answer(
        "✅ Бот работает корректно.\n\nСледующий шаг — добавить твою воронку."
    )
    await call.answer()

# ===== ЗАПУСК =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
