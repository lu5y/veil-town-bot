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
            return 
    
    state = GameState(chat_id)
    notifier = Notifier(context.bot, chat_id)
    engine = GameEngine(state, notifier)
    SESSIONS[chat_id] = (state, engine)
    
    join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
    await context.bot.send_message(chat_id, Narrator.opening(), reply_markup=join_btn, parse_mode='Markdown')
    await engine.start_lobby()

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

# --- PRIVATE COMMANDS (NEW) ---

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
    await query.answer()
    chat_id = update.effective_chat.id
    user = query.from_user
    
    if chat_id not in SESSIONS: return
    state, engine = SESSIONS[chat_id]
    
    if engine.phase != Phase.LOBBY: return

    if user.id not in state.players:
        state.players[user.id] = Player(user.id, user.first_name)
        # Using a quieter confirmation (toast notification) instead of spamming group
        await context.bot.answer_callback_query(query.id, text=f"Welcome to Veil Town, {user.first_name}.")

async def cb_handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    state, _ = find_session(user_id)
    if not state: return
    
    if data.startswith("night:"):
        target = int(data.split(":")[1])
        state.record_night_action(user_id, target, "generic") 
        await query.edit_message_text("🌑 Choice locked in darkness.")
        
    elif data.startswith("vote:"):
        target = int(data.split(":")[1])
        state.votes[user_id] = target
        # Silent confirmation for votes to keep suspense
    
