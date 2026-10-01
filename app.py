import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")
if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is missing")

bot = Bot(TOKEN)
dp = Dispatcher()
app = FastAPI()

# ==================================================
# МЕНЯЙ ТОЛЬКО ЭТОТ БЛОК — ТВОИ ВОПРОСЫ И КНОПКИ
# ==================================================
QUESTIONS = [
    {
        "question": "Какой вариант свидания ты выберешь? ❤️",
        "answers": [
            "Прогулка 🌙",
            "Кино 🎬",
            "Ресторан 🍝",
            "Куда угодно, лишь бы вместе 🥰",
        ],
    },
    {
        "question": "Куда бы ты хотела поехать со мной? ✈️",
        "answers": [
            "На море 🌊",
            "В горы 🏔️",
            "В Париж 🗼",
            "В секретное место ❤️",
        ],
    },
    {
        "question": "Что тебе больше всего нравится во мне? 😏",
        "answers": [
            "Характер ❤️",
            "Улыбка 😊",
            "Глаза 👀",
            "Всё сразу 🥰",
        ],
    },
    {
        "question": "Последний вопрос... Ты меня любишь? ❤️",
        "answers": [
            "Да ❤️",
            "Очень ❤️❤️",
            "Конечно 🥰",
            "А как иначе? 😏",
        ],
    },
]

progress = {}


def make_keyboard(number):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"answer:{number}:{i}",
                )
            ]
            for i, answer in enumerate(QUESTIONS[number]["answers"])
        ]
    )


async def show_question(chat_id, user_id):
    number = progress.get(user_id, 0)

    if number >= len(QUESTIONS):
        await bot.send_message(
            chat_id,
            "🎉 Ты закончила!\n\n"
            "Спасибо за ответы ❤️\n\n"
            "А теперь главное:\n"
            "Ты мне очень дорога 🥰",
        )
        return

    q = QUESTIONS[number]

    await bot.send_message(
        chat_id,
        f"💌 Вопрос {number + 1}/{len(QUESTIONS)}\n\n{q['question']}",
        reply_markup=make_keyboard(number),
    )


@dp.message(CommandStart())
async def start(message):
    progress[message.from_user.id] = 0

    await message.answer(
        "Привет ❤️\n\n"
        "Я приготовил для тебя небольшой тест.\n"
        "Отвечай честно 😏"
    )

    await show_question(message.chat.id, message.from_user.id)


@dp.callback_query(F.data.startswith("answer:"))
async def answer(callback):
    _, q_number, answer_number = callback.data.split(":")
    q_number = int(q_number)

    user_id = callback.from_user.id

    if progress.get(user_id, 0) != q_number:
        await callback.answer("Этот вопрос уже пройден ❤️")
        return

    progress[user_id] = q_number + 1

    await callback.answer("Ответ принят ❤️")
    await show_question(callback.message.chat.id, user_id)


@app.get("/")
async def home():
    return {"status": "ok", "message": "Girlfriend bot is running ❤️"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.on_event("startup")
async def startup():
    await bot.set_webhook(f"{WEBHOOK_URL}/telegram")


@app.on_event("shutdown")
async def shutdown():
    await bot.delete_webhook()
    await bot.session.close()
