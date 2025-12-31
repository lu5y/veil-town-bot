import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import BOT_TOKEN

from core.game_engine import GameEngine
from core.notifier import Notifier

from game.models import GameState, Player
from game.roles import ALL_ROLES


# ---------------------------------
# GLOBAL SESSION STORAGE (per group)
# ---------------------------------
SESSIONS = {}  # chat_id -> (GameState, GameEngine)


# ---------------------------------
# HELPERS
# ---------------------------------
def get_session(chat_id):
    return SESSIONS.get(chat_id)


def is_admin(update: Update):
    member = update.effective_chat.get_member(update.effective_user.id)
    return member.status in ("administrator", "creator")


# ---------------------------------
# COMMANDS
# ---------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    state = GameState(chat_id)
    notifier = Notifier(context.bot, chat_id)
    engine = GameEngine(state, notifier)

    SESSIONS[chat_id] = (state, engine)

    await engine.start_lobby()


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    if not session:
        return

    state, _ = session
    user = update.effective_user

    if user.id in state.players:
        return

    state.players[user.id] = Player(user.id, user.first_name)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"{user.first_name} joined the town."
    )


async def extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    if not session:
        return

    _, engine = session
    await engine.extend_wait()


async def force_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    if not session:
        return

    _, engine = session
    await engine.force_start()


# ---------------------------------
# CALLBACKS (BUTTONS)
# ---------------------------------
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    # Find session
    session = None
    for state, engine in SESSIONS.values():
        if user_id in state.players:
            session = (state, engine)
            break

    if not session:
        return

    state, _ = session

    # -----------------------------
    # NIGHT ACTION
    # -----------------------------
    if data.startswith("night:"):
        target_id = int(data.split(":")[1])
        state.record_night_action(user_id, target_id)

        await query.edit_message_text(
            "Your choice is locked."
        )

    # -----------------------------
    # VOTE
    # -----------------------------
    elif data.startswith("vote:"):
        target_id = int(data.split(":")[1])
        state.record_vote(user_id, target_id)

        await query.edit_message_text(
            "Your vote has been cast."
        )


# ---------------------------------
# BOOTSTRAP
# ---------------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("extend", extend))
    app.add_handler(CommandHandler("forcestart", force_start))

    # buttons
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("Veil Town engine is live.")
    app.run_polling()


if __name__ == "__main__":
    main()
