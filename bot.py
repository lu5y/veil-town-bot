import random
from game.models import Phase
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
from game.models import Player
from game.roles import ROLES

sessions = SessionManager()

# -------- BASIC COMMANDS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🩸 Veil Town\n\n"
        "/join — enter the town\n"
        "/begin — seal the town (5–15 players)\n"
        "/discussion — start discussion\n"
        "/enddiscussion — end discussion"
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    game = sessions.get_game(chat_id)

    if game.started:
        await update.message.reply_text("The town is sealed.")
        return

    if user.id in game.players:
        await update.message.reply_text("You are already in.")
        return

    game.players[user.id] = Player(user.id, user.first_name)
    await update.message.reply_text(f"{user.first_name} joined the town.")

async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = sessions.get_game(chat_id)

    if game.started:
        await update.message.reply_text("Game already started.")
        return

    count = len(game.players)
    if count < 5 or count > 15:
        await update.message.reply_text("Need 5–15 players.")
        return
async def game_engine(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    game = sessions.get_game(chat_id)

    while game.started:
        if game.phase == Phase.DISCUSSION:
            # Reset discussion tracking
            for p in game.players.values():
                p.spoke = False

            await context.bot.send_message(
                chat_id=chat_id,
                text="🗣️ Discussion Phase has begun.\nYou have 2 minutes."
            )

            # Discussion timer
            await asyncio.sleep(120)

            silent = [p.name for p in game.players.values() if not p.spoke]

            if silent:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⏳ Discussion ended.\nSilent players:\n" +
                         "\n".join(f"- {n}" for n in silent)
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="⏳ Discussion ended.\nEveryone spoke."
                )

            # Move to next phase (future)
            game.phase = Phase.NIGHT
            break

    roles = random.sample(ROLES, count)

    for player, role in zip(game.players.values(), roles):
        player.role = role
        await context.bot.send_message(
            chat_id=player.user_id,
            text=f"🩸 Your role: {role}\nTrust no one."
        )

    game.started = True
    game.phase = "LOBBY"

    await update.message.reply_text("🌑 The town is sealed.")

# -------- DISCUSSION PHASE --------

async def discussion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = sessions.get_game(chat_id)

    if not game.started:
        await update.message.reply_text("Game not started.")
        return

    game.phase = "DISCUSSION"
    for p in game.players.values():
        p.spoke = False

    await update.message.reply_text(
        "🗣️ Discussion started.\nTalk freely.\nSilence will be remembered."
    )

async def track_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    game = sessions.get_game(chat_id)

    if game.phase == "DISCUSSION" and user.id in game.players:
        game.players[user.id].spoke = True

async def enddiscussion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = sessions.get_game(chat_id)

    if game.phase != "DISCUSSION":
        await update.message.reply_text("No active discussion.")
        return

    silent = [p.name for p in game.players.values() if not p.spoke]
    game.phase = "POST"

    if silent:
        await update.message.reply_text(
            "⏳ Discussion ended.\nSilent players:\n" +
            "\n".join(f"- {n}" for n in silent)
        )
    else:
        await update.message.reply_text("⏳ Discussion ended.\nEveryone spoke.")

# -------- MAIN --------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("begin", begin))
    app.add_handler(CommandHandler("discussion", discussion))
    app.add_handler(CommandHandler("enddiscussion", enddiscussion))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_speech))

    print("Veil Town running...")
    app.run_polling()

if __name__ == "__main__":
    main()
