import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai_client import init_client
from handlers import init_allowed, cmd_start, cmd_help, cmd_history, cmd_clear, handle_text

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USER_ID_1 = os.getenv("USER_ID_1")
USER_ID_2 = os.getenv("USER_ID_2")

if not all([TELEGRAM_TOKEN, GEMINI_API_KEY, USER_ID_1, USER_ID_2]):
    raise ValueError("Заполни все переменные: TELEGRAM_TOKEN, GEMINI_API_KEY, USER_ID_1, USER_ID_2")

init_client(GEMINI_API_KEY)
init_allowed(USER_ID_1, USER_ID_2)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", cmd_start))
app.add_handler(CommandHandler("help", cmd_help))
app.add_handler(CommandHandler("history", cmd_history))
app.add_handler(CommandHandler("clear", cmd_clear))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    print("Бот запущен...")
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_polling()
