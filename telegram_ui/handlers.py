from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from game.models import GameState, Player
from core.game_engine import GameEngine, Phase
from core.narrator import Narrator
from core.notifier import Notifier

SESSIONS = {}

# --- HELPER: Find user's session ---
def find_session(user_id):
    for state, engine in SESSIONS.values():
        if user_id in state.players:
            return state, engine
    return None, None

# --- GROUP COMMANDS ---

async def cmd_start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in SESSIONS:
        state, engine = SESSIONS[chat_id]
        if engine.phase != Phase.GAME_OVER:
            await context.bot.send_message(chat_id, "⚠️ A game is already running. Use /killgame to force stop it.")
            return 
    
    state = GameState(chat_id)
    notifier = Notifier(context.bot, chat_id)
    engine = GameEngine(state, notifier)
    SESSIONS[chat_id] = (state, engine)
    
    join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
    await context.bot.send_message(chat_id, Narrator.opening(), reply_markup=join_btn, parse_mode='Markdown')
    await engine.start_lobby()

async def cmd_kill_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forcefully removes the game session."""
    chat_id = update.effective_chat.id
    if chat_id in SESSIONS:
        del SESSIONS[chat_id]
        await context.bot.send_message(chat_id, "💀 **Game killed.** State wiped. You may start anew.")
    else:
        await context.bot.send_message(chat_id, "No active game found to kill.")

async def cmd_force_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SESSIONS: return
    _, engine = SESSIONS[chat_id]
    await engine.force_start()

async def cmd_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SESSIONS: return
    state, _ = SESSIONS[chat_id]
    alive = [f"• {p.name}" for p in state.players.values() if p.is_alive]
    msg = "**The Living:**\n" + "\n".join(alive) if alive else "All are dead."
    await context.bot.send_message(chat_id, msg, parse_mode='Markdown')

async def cmd_extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SESSIONS: return
    await context.bot.send_message(chat_id, "⏳ **Time extended.**", parse_mode='Markdown')

# --- PRIVATE COMMANDS ---

async def cmd_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state, _ = find_session(user_id)
    
    if not state:
        await context.bot.send_message(user_id, "You are not in a town.")
        return

    player = state.players[user_id]
    if player.role:
        await context.bot.send_message(user_id, Narrator.role_dm(player.role), parse_mode='Markdown')
    else:
        await context.bot.send_message(user_id, "Roles have not been assigned yet.")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state, engine = find_session(user_id)
    
    if not engine:
        await context.bot.send_message(user_id, "You are not in a game.")
        return

    await context.bot.send_message(user_id, Narrator.help_text(engine.phase))

# --- BUTTON HANDLERS ---

async def cb_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    chat_id = update.effective_chat.id
    user = query.from_user
    
    # ERROR HANDLING: If bot restarted, session is gone
    if chat_id not in SESSIONS:
        await query.answer("This game has expired. Start a new one with /startgame", show_alert=True)
        return

    state, engine = SESSIONS[chat_id]
    
    if engine.phase != Phase.LOBBY:
        await query.answer("Game has already started!", show_alert=True)
        return

    if user.id not in state.players:
        state.players[user.id] = Player(user.id, user.first_name)
        await query.answer(f"Welcome to Veil Town, {user.first_name}.")
        # Optional: Send a visible message so others see the join count
        # await context.bot.send_message(chat_id, f"{user.first_name} enters.")
    else:
        await query.answer("You are already in.")

async def cb_handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    state, _ = find_session(user_id)
    
    # ERROR HANDLING: If session is missing (bot restarted)
    if not state:
        await query.answer("Session not found. The town has faded.", show_alert=True)
        return
    
    if data.startswith("night:"):
        try:
            target = int(data.split(":")[1])
            state.record_night_action(user_id, target, "generic") 
            await query.edit_message_text("🌑 Choice locked in darkness.")
            await query.answer() # Close the load spinner
        except Exception:
            await query.answer("Error recording action.", show_alert=True)
        
    elif data.startswith("vote:"):
        target = int(data.split(":")[1])
        state.votes[user_id] = target
        await query.answer("Vote cast.") # Feedback to user
        # We do NOT edit the message here to keep votes secret until the end
        
