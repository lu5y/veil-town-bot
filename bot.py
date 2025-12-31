import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from core.session_manager import SessionManager
from game.models import Player, Phase
from game.roles import ROLES

# --------------------
# GLOBAL SESSION STORE
# --------------------
sessions = SessionManager()

# --------------------
# BASIC COMMANDS
# --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🩸 Veil Town\n\n"
        "/join — enter the town\n"
        "/begin — seal the town (5–15 players)"
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    game = sessions.get_game(chat_id)

    if game.started:
        await update.message.reply_text("The town is sealed. You cannot enter.")
        return

    if user.id in game.players:
        await update.message.reply_text("You are already in the town.")
        return

    game.players[user.id] = Player(
        user_id=user.id,
        name=user.first_name
    )

    await update.message.reply_text(f"{user.first_name} has entered the town.")

async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = sessions.get_game(chat_id)

    if game.started:
        await update.message.reply_text("The game has already started.")
        return

    count = len(game.players)
    if count < 5 or count > 15:
        await update.message.reply_text("The game requires 5–15 players.")
        return

    roles = random.sample(ROLES, count)

    for player, role in zip(game.players.values(), roles):
        player.role = role
        await context.bot.send_message(
            chat_id=player.user_id,
            text=f"🩸 Your role: {role}\nTrust no one."
        )

    game.started = True
    game.phase = Phase.DISCUSSION

    await update.message.reply_text(
        "🌑 The town is sealed.\nThe game begins."
    )

    # START THE GAME ENGINE
    context.application.create_task(
        game_engine(chat_id, context)
    )

# --------------------
# MESSAGE TRACKING
# --------------------

async def track_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    game = sessions.get_game(chat_id)

    if game.phase == Phase.DISCUSSION and user.id in game.players:
        game.players[user.id].spoke = True

# --------------------
# GAME ENGINE
# --------------------

async def game_engine(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    game = sessions.get_game(chat_id)

    while game.started:

        # --------------------
        # DISCUSSION PHASE
        # --------------------
        if game.phase == Phase.DISCUSSION:

            # Reset discussion flags
            for p in game.players.values():
                p.spoke = False

            await context.bot.send_message(
                chat_id=chat_id,
                text="🗣️ Discussion Phase has begun.\nYou have 2 minutes."
            )

            # Discussion timer
            await asyncio.sleep(120)

            silent_players = [
                p.name for p in game.players.values() if not p.spoke
            ]

            if silent_players:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⏳ Discussion ended.\nSilent players:\n" +
                         "\n".join(f"- {name}" for name in silent_players)
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⏳ Discussion ended.\nEveryone spoke."
                )

            # TEMPORARY STOP (next phases added later)
            await context.bot.send_message(
                chat_id=chat_id,
                text="🌘 Night will fall soon...\n(To be implemented)"
            )

            break  # Stop engine for now (professional, intentional)

# --------------------
# MAIN
# --------------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("begin", begin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_speech))

    print("🩸 Veil Town is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
