import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

# ===== ТОКЕН БОТА =====
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN не задан")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ===== ССЫЛКИ =====
CHANNEL_LINK = "https://t.me/personalcode3"

VIDEO_LINKS = {
    1: "VIDEO_LINK_VECTOR_1",
    2: "VIDEO_LINK_VECTOR_2",
    3: "VIDEO_LINK_VECTOR_3",
    4: "VIDEO_LINK_VECTOR_4",
}

user_answers = {}

# ===== СТАРТ =====
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 УЗНАТЬ СВОЙ АРХЕТИП", callback_data="q1")
    )
    await message.answer(
        "Привет! 👋\n\nХочешь узнать свой денежный вектор?\n\nОтветь на 6 вопросов 👇",
        reply_markup=kb
    )

# ===== ВОПРОСЫ =====
QUESTIONS = {
    "q1": "Что тебя больше всего мотивирует?",
    "q2": "Как тебе комфортнее работать?",
    "q3": "Как ты относишься к риску?",
    "q4": "Что для тебя главное в деньгах?",
    "q5": "Как реагируешь на препятствия?",
    "q6": "Какой доход тебе ближе?",
}

NEXT_Q = {
    "q1": "q2",
    "q2": "q3",
    "q3": "q4",
    "q4": "q5",
    "q5": "q6",
}

def answer_kb(q):
    kb = InlineKeyboardMarkup()
    for i in range(1, 5):
        kb.add(InlineKeyboardButton(str(i), callback_data=f"{q}_{i}"))
    return kb

@dp.callback_query_handler(lambda c: c.data.startswith("q"))
async def process_answers(call: types.CallbackQuery):
    q, ans = call.data.split("_")
    user_answers.setdefault(call.from_user.id, []).append(int(ans))

    if q != "q6":
        await call.message.edit_text(
            QUESTIONS[NEXT_Q[q]],
            reply_markup=answer_kb(NEXT_Q[q])
        )
    else:
        await show_result(call)

# ===== РЕЗУЛЬТАТ =====
async def show_result(call):
    answers = user_answers[call.from_user.id]
    vector = max(set(answers), key=answers.count)

    texts = {
        1: "💥 Твой вектор — ДЕЙСТВИЕ И ЛИДЕРСТВО",
        2: "🎨 Твой вектор — ТВОРЧЕСТВО И ВДОХНОВЕНИЕ",
        3: "📊 Твой вектор — СИСТЕМА И ЭКСПЕРТНОСТЬ",
        4: "🌍 Твой вектор — СВОБОДА И ПОТОК",
    }

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📺 Смотреть видео", url=VIDEO_LINKS[vector]))
    kb.add(InlineKeyboardButton("📲 Перейти в канал", url=CHANNEL_LINK))

    await call.message.answer(texts[vector], reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
