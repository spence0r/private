# 💕 Telegram-бот для девушки — запуск с iPhone

Этот вариант работает через webhook и подходит для облачного запуска.

## Что понадобится

- iPhone
- Telegram
- GitHub
- Render
- токен от @BotFather

Windows/Mac не нужны.

## Файлы

Загрузить в GitHub нужно:

- app.py
- requirements.txt

## Render

Создай на Render новый Web Service из GitHub.

Build Command:

pip install -r requirements.txt

Start Command:

uvicorn app:app --host 0.0.0.0 --port $PORT

Выбери Free.

После первого запуска Render даст адрес вида:

https://your-bot.onrender.com

В Environment добавь:

BOT_TOKEN = токен от BotFather

WEBHOOK_URL = https://your-bot.onrender.com

После сохранения Render перезапустит приложение.

Открой своего бота в Telegram и отправь /start.

## Изменение вопросов

В app.py найди QUESTIONS.

Меняй только этот блок.

После изменения файла в GitHub Render автоматически задеплоит новую версию.

## Важно

WEBHOOK_URL должен быть ровно адресом Render без /telegram в конце.

Не публикуй BOT_TOKEN.
