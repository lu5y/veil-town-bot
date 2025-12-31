# bot.py
# Entry point for Veil Town Telegram Bot

import os
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from core.engine import GameEngine
from telegram_ui.commands import (
    start,
    startgame,
    join,
    extend,
    force_start,
)

# ----------------------------
# LOGGING
# ----------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ----------------------------
# BOT SETUP
# ----------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

engine = GameEngine()


async def on_startup(app):
    # store engine globally for handlers
    app.bot_data["engine"] = engine
    logger.info("Veil Town bot started.")


# ----------------------------
# MAIN
# ----------------------------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startgame", startgame))
    app.add_handler(CommandHandler("forcestart", force_start))

    # Buttons / callbacks
    app.add_handler(CallbackQueryHandler(join, pattern="^join_game$"))
    app.add_handler(CallbackQueryHandler(extend, pattern="^extend_lobby$"))
    app.add_handler(CallbackQueryHandler(force_start, pattern="^force_start$"))

    app.run_polling()


if __name__ == "__main__":
    main()
