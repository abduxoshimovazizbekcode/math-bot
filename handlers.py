from telegram import Update
from telegram.ext import ContextTypes
from openai_client import ask_text
from memory import clear_history, get_last_n

ALLOWED_IDS: set[int] = set()


def init_allowed(user_id_1: str, user_id_2: str) -> None:
    ALLOWED_IDS.add(int(user_id_1))
    ALLOWED_IDS.add(int(user_id_2))


def _is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_IDS


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа.")
        return
    await update.message.reply_text(
        "Привет! Я математический ассистент на базе Gemini 2.0 Flash.\n\n"
        "📝 Отправь задачу — решу пошагово.\n"
        "🔍 Спроси про тему — объясню и найду информацию.\n"
        "📚 Попроси рассказать про раздел математики — дам обзор.\n\n"
        "Команды: /help /history /clear"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа.")
        return
    await update.message.reply_text(
        "Как пользоваться:\n\n"
        "📝 Задачи:\n"
        "  «Найди корни уравнения x²-5x+6=0»\n"
        "  «Вычисли интеграл от x² dx»\n\n"
        "🔍 Темы и понятия:\n"
        "  «Что такое производная?»\n"
        "  «Расскажи про теорему Пифагора»\n"
        "  «Что изучает теория вероятностей?»\n\n"
        "📚 Поиск информации:\n"
        "  «Кто такой Эйлер и что он открыл?»\n"
        "  «Где применяется линейная алгебра?»\n\n"
        "• /history — последние 5 сообщений\n"
        "• /clear — очистить общую историю"
    )


async def cmd_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа.")
        return
    messages = get_last_n(5)
    if not messages:
        await update.message.reply_text("История пуста.")
        return
    lines = []
    for m in messages:
        role = "Вы" if m["role"] == "user" else "Бот"
        text = m["content"] if isinstance(m["content"], str) else "[составное]"
        lines.append(f"[{role}]: {text[:200]}")
    await update.message.reply_text("\n\n".join(lines))


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа.")
        return
    clear_history()
    await update.message.reply_text("История очищена.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа.")
        return
    user_text = update.message.text.strip()
    if not user_text:
        return
    await update.message.reply_text("Решаю...")
    try:
        answer = await ask_text(user_text)
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
