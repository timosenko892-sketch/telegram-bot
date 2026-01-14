import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "8494561103:AAFGnUkQmIKHNuKbX0nxXqZvgq3ppGijcbk"

# ===== ЮKASSA (ВСТАВИШЬ ПОТОМ) =====
PAYMENT_PROVIDER_TOKEN = "PASTE_YOOKASSA_TOKEN_HERE"
PRICE = 99900  # 999 руб

# ===== ССЫЛКИ (МЕНЯЕШЬ САМА) =====
CHANNEL_LINK = "https://t.me/personalcode3"

VIDEO_LINKS = {
    1: "VIDEO_LINK_VECTOR_1",
    2: "VIDEO_LINK_VECTOR_2",
    3: "VIDEO_LINK_VECTOR_3",
    4: "VIDEO_LINK_VECTOR_4",
}

GUIDE_PDF = "LINK_TO_PDF"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_answers = {}

# ===== СТАРТ =====
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🚀 УЗНАТЬ СВОЙ АРХЕТИП", callback_data="q1")
    )
    await message.answer(
        "Привет! 👋\n\nХочешь узнать свой денежный магнит?\n\n6 вопросов — и твой код раскроется.",
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
    "q1": "q2", "q2": "q3", "q3": "q4",
    "q4": "q5", "q5": "q6"
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
        next_q = NEXT_Q[q]
        await call.message.edit_text(
            QUESTIONS[next_q],
            reply_markup=answer_kb(next_q)
        )
    else:
        await show_result(call)

# ===== РЕЗУЛЬТАТ =====
async def show_result(call):
    answers = user_answers[call.from_user.id]
    vector = max(set(answers), key=answers.count)

    texts = {
        1: "💥 Твой вектор — ДЕЙСТВИЕ И ЛИДЕРСТВО...",
        2: "🎨 Твой вектор — ТВОРЧЕСТВО И ВДОХНОВЕНИЕ...",
        3: "📊 Твой вектор — СИСТЕМА И ЭКСПЕРТНОСТЬ...",
        4: "🌍 Твой вектор — СВОБОДА И ПОТОК..."
    }

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📺 Смотреть видео", url=VIDEO_LINKS[vector]),
        InlineKeyboardButton("💎 Забрать гайд", callback_data="buy")
    )

    await call.message.answer(
        texts[vector],
        reply_markup=kb
    )

# ===== ОПЛАТА =====
@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(call: types.CallbackQuery):
    prices = [types.LabeledPrice(label="Гайд Магнит для денег", amount=PRICE)]
    await bot.send_invoice(
        call.from_user.id,
        title="Гайд «Магнит для денег»",
        description="Персональный разбор денежного вектора",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        payload="guide"
    )

@dp.pre_checkout_query_handler(lambda q: True)
async def checkout(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def success(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("📥 Скачать гайд", url=GUIDE_PDF)
    )
    await message.answer("Оплата принята! 🎉", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
