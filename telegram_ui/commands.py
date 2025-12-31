# telegram_ui/commands.py
# Telegram command handlers (UI layer only)

from telegram import Update
from telegram.ext import ContextTypes

from narrative.system_text import (
    START_PRIVATE,
    START_GROUP,
    ERROR_GAME_RUNNING,
    ERROR_NO_GAME,
)
from telegram_ui.messages import simple_notice
from telegram_ui.buttons import (
    join_lobby_button,
    extend_lobby_button,
    force_start_button,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text(START_PRIVATE)
    else:
        await update.message.reply_text(START_GROUP)


async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    engine = context.application.bot_data.get("engine")

    if engine.has_game(chat_id):
        await update.message.reply_text(ERROR_GAME_RUNNING)
        return

    engine.create_game(chat_id)

    await update.message.reply_text(
        simple_notice("Lobby opened."),
        reply_markup=join_lobby_button(),
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    user = query.from_user

    engine = context.application.bot_data.get("engine")

    if not engine.has_game(chat_id):
        await query.answer("No active lobby.")
        return

    engine.add_player(chat_id, user)
    await query.answer("You joined the game.")


async def extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id

    engine = context.application.bot_data.get("engine")
    engine.extend_lobby(chat_id)

    await query.answer("Lobby extended.")


async def force_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    engine = context.application.bot_data.get("engine")

    if not engine.has_game(chat_id):
        await update.message.reply_text(ERROR_NO_GAME)
        return

    engine.force_start(chat_id)
    await update.message.reply_text(simple_notice("Game forced to start."))
