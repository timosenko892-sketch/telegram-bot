import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Токен бота
API_TOKEN = os.getenv("API_TOKEN", "8494561103:AAFGnUkQmIKHNuKbX0nxXqZvgq3ppGijcbk")

# Ссылки
VIDEO_LINKS = {
    1: "https://example.com/video1",
    2: "https://example.com/video2",
    3: "https://example.com/video3",
    4: "https://example.com/video4",
}

logging.basicConfig(level=logging.INFO)
user_answers = {}

# ===== СТАРТ =====
async def start(update: Update, context: CallbackContext):
    kb = [[InlineKeyboardButton("🚀 УЗНАТЬ СВОЙ АРХЕТИП", callback_data="q1")]]
    await update.message.reply_text(
        "Привет! 👋\n\nХочешь узнать свой денежный магнит?\n\n6 вопросов — и твой код раскроется.",
        reply_markup=InlineKeyboardMarkup(kb)
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
    kb = []
    for i in range(1, 5):
        kb.append([InlineKeyboardButton(str(i), callback_data=f"{q}_{i}")])
    return InlineKeyboardMarkup(kb)

# ===== ОБРАБОТКА ОТВЕТОВ =====
async def process_answers(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    q, ans = query.data.split("_")
    user_id = query.from_user.id
    user_answers.setdefault(user_id, []).append(int(ans))

    if q != "q6":
        next_q = NEXT_Q[q]
        await query.edit_message_text(
            QUESTIONS[next_q],
            reply_markup=answer_kb(next_q)
        )
    else:
        await show_result(query)

# ===== РЕЗУЛЬТАТ =====
async def show_result(query):
    answers = user_answers[query.from_user.id]
    vector = max(set(answers), key=answers.count)

    texts = {
        1: "💥 Твой вектор — ДЕЙСТВИЕ И ЛИДЕРСТВО...",
        2: "🎨 Твой вектор — ТВОРЧЕСТВО И ВДОХНОВЕНИЕ...",
        3: "📊 Твой вектор — СИСТЕМА И ЭКСПЕРТНОСТЬ...",
        4: "🌍 Твой вектор — СВОБОДА И ПОТОК..."
    }

    kb = [
        [InlineKeyboardButton("📺 Смотреть видео", url=VIDEO_LINKS[vector])],
        [InlineKeyboardButton("📥 Получить гайд (скоро)", callback_data="soon")]
    ]

    await query.edit_message_text(
        texts[vector],
        reply_markup=InlineKeyboardMarkup(kb)
    )

# ===== ЗАГЛУШКА =====
async def soon(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer("Гайд будет доступен в ближайшее время! 🔜", show_alert=True)

# ===== ЗАПУСК =====
def main():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(process_answers, pattern="^q"))
    app.add_handler(CallbackQueryHandler(soon, pattern="^soon$"))
    app.run_polling()

if __name__ == "__main__":
    main()
