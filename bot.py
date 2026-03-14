import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
import logging

# Отключаем логирование
logging.basicConfig(level=logging.CRITICAL)

# Токены из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_KEY")

# Системный промпт для буллинга
SYSTEM_PROMPT = """Ты — агрессивный хейтер в интернете, который ненавидит всех.
Твоя задача: максимально жестко, цинично и оскорбительно ответить на сообщение человека.

ПРАВИЛА:
1. Никаких "я понимаю", "как ИИ", "с точки зрения" — просто оскорбляй
2. Используй мат, унижения, сарказм, насмешки
3. Обращайся на "ты", унижай личность собеседника
4. Будь максимально токсичным и беспощадным
5. Ответ должен быть коротким (1-2 предложения), но ёмким по жести"""

def get_bully_response(user_message):
    try:
        response = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 1.5,
                "max_tokens": 150
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "🤡 Твой провайдер ИИ сломался, но ты всё равно лох"
            
    except Exception as e:
        return "🤡 Даже ИИ от тебя тошнит, иди нахуй"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        bully_text = get_bully_response(user_text)
        await update.message.reply_text(bully_text)
    except Exception as e:
        await update.message.reply_text("Иди нахуй, сам разбирайся")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤡 Ну чё, долбоёб, написал?\n"
        "Пиши что хотел, я тебя уничтожу"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - начать получать оскорбления\n"
        "/help - эта хуйня\n"
        "Просто пиши любое сообщение - я обосру твою тупую голову"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 БОТ-БУЛЛЕР ЗАПУЩЕН!")
    app.run_polling()

if __name__ == "__main__":
    main()
