import os

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Update,
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from dotenv import load_dotenv


# ============================================================
# НАСТРОЙКИ
# ============================================================

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


# ============================================================
# ТЕКСТЫ
# ============================================================

INTRO = """Привет, это Никита. Я писал этот тест около 2-х суток, но надеюсь тебе понравится.

Прямо сейчас я написал тебе сообщение, с чем связан один из моих сюрпризов, чтоб ты не переживала.

Вопросы максимально разбросаны, но в основном они касаются меня
(да, я ЧСВ уебище)"""


RULES = """📜 СВОД ПРАВИЛ

1) Тест написан с любовью, без злого умысла и не несет цели кого либо оскорбить;

2) Нажимая кнопку «Приступить к тесту», Вы обязуетесь сдать своему парню свою сумку и подик;

3) Тест содержит вопросы на которые Вы знаете ответ;

4) Запрещено пользоваться интернетом и помощью Леры;

5) Для получения подсказки обратитесь к создателю теста (своему парню) и скажите:
«Нужна подсказка»,
а затем поцелуйте ❤️"""


FINAL_MESSAGE = """Никита тебя очень сильно любит и хочет, чтоб это был не первый и не последний приятный момент в твоей жизни рядом с ним ❤️‍🔥"""


# ============================================================
# ВОПРОСЫ
# ============================================================

QUESTIONS = {

    1: {
        "type": "correct",
        "question": "Когда мы познакомились?",
        "answers": [
            "Сентябрь 2024",
            "Сентябрь 2025",
            "Ноябрь 2024",
            "Июнь 2026",
        ],
        "correct": "Сентябрь 2025",
    },

    2: {
        "type": "correct",
        "question": "Кого я люблю слушать больше всего?",
        "answers": [
            "Friendly Thug 52 NGG",
            "вышел покурить",
            "Лавлинская Маргарита Евгеньевна",
            "Всех сразу",
        ],
        "correct": "Лавлинская Маргарита Евгеньевна",
    },

    3: {
        "type": "correct",
        "question": "Какой любимый цвет у твоего парня?",
        "answers": [
            "Черный",
            "Белый",
            "Красный",
            "Синий",
        ],
        "correct": "Черный",
    },

    4: {
        "type": "correct",
        "question": "На какой марке машины твой парень получает права?",
        "answers": [
            "Volkswagen Polo",
            "Koenigsegg Gemera",
            "Pagani Huayra",
            "Lada 2121",
        ],
        "correct": "Volkswagen Polo",
    },

    5: {
        "type": "correct",
        "question": "Какой характер у твоего парня?",
        "answers": [
            "Добрый",
            "Сдержанный",
            "Дурак",
            "Конченный дурак, который не умеет делать сюрпризы",
        ],
        "correct": "Конченный дурак, который не умеет делать сюрпризы",
    },

    6: {
        "type": "correct",
        "question": "Какая главная цель в жизни у твоего парня?",
        "answers": [
            "Построить карьеру успешного киберспортсмена",
            "Завести счастливую семью с тобой",
            "Радовать тебя каждый день, несмотря на недопонимания и ссоры",
            "Все сразу",
        ],
        "correct": "Все сразу",
    },

    7: {
        "type": "correct",
        "question": "За какую команду по CS2 болеет твой парень?",
        "answers": [
            "Team Vitality",
            "Team Spirit",
            "Parivision",
            "Team Falcons",
        ],
        "correct": "Team Spirit",
    },

    8: {
        "type": "correct",
        "question": "Что первым сделает твой парень после получения водительских прав и покупки машины?",
        "answers": [
            "Поедет гонять 200+ км/ч по дворам",
            "Поедет по телкам",
            "Поедет к Еве",
            "Поедет кататься с тобой под твои любимые треки",
        ],
        "correct": "Поедет кататься с тобой под твои любимые треки",
    },

    9: {
        "type": "correct",
        "question": "Как зовут твоего парня?",
        "answers": [
            "Вадим",
            "Даниил",
            "Ваня",
            "Никита",
        ],
        "correct": "Никита",
    },

    10: {
        "type": "correct",
        "question": "Сколько Вы встречаетесь?",
        "answers": [
            "1 год",
            "2 месяца",
            "5 лет",
            "1 неделю",
        ],
        "correct": "2 месяца",
    },

    # ========================================================
    # БЕЗ ПРАВИЛЬНОГО ОТВЕТА
    # ========================================================

    11: {
        "type": "normal",
        "question": "Тебе нравится характер твоего парня?",
        "answers": [
            "Да",
            "Нет",
        ],
    },

    12: {
        "type": "normal",
        "question": "Как ты думаешь, он опять облажался и нихуя толкового не сделал, или это не единственный сюрприз?",
        "answers": [
            "Облажался, это в его стиле",
            "Он подготовился, он меня сильно любит",
        ],
    },

    13: {
        "type": "normal",
        "question": "Ты чувствуешь его любовь когда он не рядом?",
        "answers": [
            "Да, даже когда ложусь спать",
            "Нет, он мне не нужен",
        ],
    },

    14: {
        "type": "normal",
        "question": "Ты видишь свое будущее рядом с ним?",
        "answers": [
            "Да",
            "Нет",
            "Ни за что",
        ],
    },

    15: {
        "type": "normal",
        "question": "Знаешь ли ты, что он конченный дурак?",
        "answers": [
            "Да, это не обсуждается",
            "Нет, вроде норм чувак",
        ],
    },

    # ========================================================
    # СНОВА ПРАВИЛЬНЫЙ ОТВЕТ
    # ========================================================

    16: {
        "type": "correct",
        "question": "Какие цветы тебе уже дарил Никита?",
        "answers": [
            "Гвоздики",
            "Розовые розы",
            "Красные розы",
            "Фиолетовые гипсофилы",
        ],
        "correct": "Розовые розы",
    },

    # ========================================================
    # СВОБОДНЫЙ ОТВЕТ
    # ========================================================

    17: {
        "type": "text",
        "question": "Как ты думаешь, что Никита приготовил тебе в виде второго сюрприза?",
    },

    18: {
        "type": "text",
        "question": "Как ты думаешь, насколько сильно тебя любит Никита, по 10-ти балльной шкале?",
    },

    # ========================================================
    # ВОПРОС 19
    # ========================================================

    19: {
        "type": "normal",
        "question": "Ты веришь в исполнение желаний и мечт?",
        "answers": [
            "Да",
            "Нет",
        ],
    },

    # ========================================================
    # ВОПРОС 20
    # ========================================================

    20: {
        "type": "correct_final",
        "question": "Какой у тебя под?",
        "answers": [
            "Smoant Charon Baby",
            "Vaporesso XROS 5 mini",
            "VooPoo Argus II",
            "GeekVape Aegis Hero II",
        ],
        "correct": "GeekVape Aegis Hero II",
    },
}


# ============================================================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЕЙ
# ============================================================

# user_id -> номер текущего вопроса
progress = {}

# user_id -> режим ожидания текста
waiting_for_text = {}


# ============================================================
# КНОПКА "ПРИСТУПИТЬ"
# ============================================================

def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❤️ Приступить к тесту",
                    callback_data="start_test",
                )
            ]
        ]
    )


# ============================================================
# КНОПКИ ОТВЕТОВ
# ============================================================

def question_keyboard(question_number):
    question = QUESTIONS[question_number]

    buttons = []

    for index, answer in enumerate(question["answers"]):
        buttons.append([
            InlineKeyboardButton(
                text=answer,
                callback_data=f"answer:{question_number}:{index}",
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ============================================================
# ПОКАЗ ВОПРОСА
# ============================================================

async def show_question(chat_id, user_id, question_number):

    question = QUESTIONS[question_number]

    if question["type"] == "text":

        waiting_for_text[user_id] = question_number

        await bot.send_message(
            chat_id,
            f"❓ Вопрос {question_number}/20\n\n"
            f"{question['question']}\n\n"
            "✍️ Напиши свой ответ сообщением:",
        )

        return

    await bot.send_message(
        chat_id,
        f"❓ Вопрос {question_number}/20\n\n"
        f"{question['question']}",
        reply_markup=question_keyboard(question_number),
    )


# ============================================================
# /START
# ============================================================

@dp.message(CommandStart())
async def start(message: Message):

    user_id = message.from_user.id

    progress[user_id] = 0
    waiting_for_text.pop(user_id, None)

    await message.answer(INTRO)

    await message.answer(
        RULES,
        reply_markup=start_keyboard(),
    )


# ============================================================
# НАЖАТИЕ "ПРИСТУПИТЬ"
# ============================================================

@dp.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery):

    user_id = callback.from_user.id

    progress[user_id] = 1
    waiting_for_text.pop(user_id, None)

    await callback.answer("Начинаем ❤️")

    await callback.message.answer(
        "Ну что, поехали 😏\n\n"
        "Помни правила. И особенно пункт №5 ❤️"
    )

    await show_question(
        callback.message.chat.id,
        user_id,
        1,
    )


# ============================================================
# ОБРАБОТКА КНОПОК
# ============================================================

@dp.callback_query(F.data.startswith("answer:"))
async def answer(callback: CallbackQuery):

    _, question_number, answer_number = callback.data.split(":")

    question_number = int(question_number)
    answer_number = int(answer_number)

    user_id = callback.from_user.id

    # Если пользователь нажал старую кнопку
    if progress.get(user_id) != question_number:

        await callback.answer(
            "Этот вопрос уже пройден ❤️",
            show_alert=True,
        )

        return

    question = QUESTIONS[question_number]

    selected_answer = question["answers"][answer_number]

    # ========================================================
    # ВОПРОС С ПРАВИЛЬНЫМ ОТВЕТОМ
    # ========================================================

    if question["type"] == "correct":

        if selected_answer != question["correct"]:

            await callback.answer(
                "Неверный ответ 😏",
                show_alert=True,
            )

            await callback.message.answer(
                "❌ Неверный ответ.\n\n"
                "Подумай ещё раз 😏"
            )

            return

        await callback.answer("Правильно! ❤️")

        await callback.message.answer(
            "✅ Правильно ❤️"
        )

    # ========================================================
    # ОБЫЧНЫЙ ВОПРОС БЕЗ ПРАВИЛЬНОГО ОТВЕТА
    # ========================================================

    elif question["type"] == "normal":

        await callback.answer("Ответ принят ❤️")

    # ========================================================
    # ВОПРОС №20
    # ========================================================

    elif question["type"] == "correct_final":

        if selected_answer != question["correct"]:

            await callback.answer(
                "Неверный ответ",
                show_alert=True,
            )

            await callback.message.answer(
                "Неверный ответ. Обратитесь к моему горе-кодеру за помощью"
            )

            # Остаёмся на вопросе 20
            return

        await callback.answer("Правильно ❤️")

        await callback.message.answer(
            "Вот теперь правильно 😏❤️"
        )

    # ========================================================
    # ПЕРЕХОД ДАЛЬШЕ
    # ========================================================

    if question_number == 19:

        progress[user_id] = 20

        await callback.message.answer(
            "Хорошо, вернемся к нашим вопросам ❤️"
        )

        await show_question(
            callback.message.chat.id,
            user_id,
            20,
        )

        return

    # Обычный переход
    next_question = question_number + 1

    progress[user_id] = next_question

    # Если это вопрос №20 и он правильный — конец
    if question_number == 20:

        progress[user_id] = 21

        await callback.message.answer(
            FINAL_MESSAGE
        )

        return

    await show_question(
        callback.message.chat.id,
        user_id,
        next_question,
    )


# ============================================================
# ОБРАБОТКА СВОБОДНОГО ТЕКСТА
# ============================================================

@dp.message(F.text)
async def text_answer(message: Message):

    user_id = message.from_user.id

    if user_id not in waiting_for_text:
        return

    question_number = waiting_for_text[user_id]

    # Сохраняем ответ в памяти.
    # При желании позже можно записывать ответы в базу.
    user_answer = message.text.strip()

    # Убираем режим ожидания
    waiting_for_text.pop(user_id, None)

    # ========================================================
    # ВОПРОС 17
    # ========================================================

    if question_number == 17:

        await message.answer(
            "Интересный вариант... 👀\n\n"
            "Ответ принят ❤️"
        )

    # ========================================================
    # ВОПРОС 18
    # ========================================================

    elif question_number == 18:

        await message.answer(
            f"Я запомнил твою оценку: {user_answer} ❤️"
        )

    # Следующий вопрос
    next_question = question_number + 1

    progress[user_id] = next_question

    await show_question(
        message.chat.id,
        user_id,
        next_question,
    )


# ============================================================
# WEBHOOK
# ============================================================

@app.get("/")
async def home():

    return {
        "status": "ok",
        "message": "Girlfriend quiz is running ❤️",
    }


@app.post("/telegram")
async def telegram_webhook(request: Request):

    data = await request.json()

    update = Update.model_validate(
        data,
        context={"bot": bot},
    )

    await dp.feed_update(
        bot,
        update,
    )

    return {"ok": True}


# ============================================================
# ЗАПУСК
# ============================================================

@app.on_event("startup")
async def startup():

    await bot.set_webhook(
        f"{WEBHOOK_URL}/telegram"
    )


@app.on_event("shutdown")
async def shutdown():

    await bot.delete_webhook()

    await bot.session.close()
