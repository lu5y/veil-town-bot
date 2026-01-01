import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatType
from telegram.ext import ContextTypes
from game.models import GameState, Player
from core.game_engine import GameEngine, Phase
from core.narrator import Narrator
from core.notifier import Notifier

logger = logging.getLogger(__name__)

SESSIONS = {}

def find_session(user_id):
    for state, engine in SESSIONS.values():
        if user_id in state.players:
            return state, engine
    return None, None

# --- COMMANDS ---

async def cmd_start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    # Block Private DMs
    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(chat.id, "🚫 **Groups only.**\nAdd me to a group to play.")
        return

    if chat.id in SESSIONS:
        state, engine = SESSIONS[chat.id]
        if engine.phase != Phase.GAME_OVER:
            await context.bot.send_message(chat.id, "⚠️ **Game Running.**\nUse /killgame first.")
            return 
    
    state = GameState(chat.id)
    notifier = Notifier(context.bot, chat.id)
    engine = GameEngine(state, notifier)
    SESSIONS[chat.id] = (state, engine)
    
    join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
    
    # 1. Send the Message ONCE
    msg = await context.bot.send_message(
        chat.id, 
        Narrator.opening([], 120), # Empty list initially
        reply_markup=join_btn, 
        parse_mode='Markdown'
    )
    
    # 2. Tell the Engine to update THIS message ID
    await engine.start_lobby(msg.message_id)

async def cmd_kill_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in SESSIONS:
        # Stop the engine loop if it's running
        try:
            _, engine = SESSIONS[chat_id]
            if engine.task: engine.task.cancel()
        except: pass
        
        del SESSIONS[chat_id]
        await context.bot.send_message(chat_id, "💀 **Game killed.**")
    else:
        await context.bot.send_message(chat_id, "ℹ️ No game found.")

async def cmd_force_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SESSIONS: return
    state, engine = SESSIONS[chat_id]
    
    # Don't start empty games
    if len(state.players) == 0:
        await context.bot.send_message(chat_id, "⚠️ **Town is empty.**")
        return
        
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
    await context.bot.send_message(chat_id, "⏳ **Time extended.**")

async def cmd_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state, _ = find_session(user_id)
    if state and state.players[user_id].role:
        await context.bot.send_message(user_id, Narrator.role_dm(state.players[user_id].role), parse_mode='Markdown')

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state, engine = find_session(user_id)
    if engine:
        await context.bot.send_message(user_id, Narrator.help_text(engine.phase))

# --- BUTTONS ---

async def cb_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = query.from_user
    
    if chat_id not in SESSIONS:
        try: await query.answer("Game expired.", show_alert=True)
        except: pass
        return

    state, engine = SESSIONS[chat_id]
    
    if engine.phase != Phase.LOBBY:
        await query.answer("Too late!", show_alert=True)
        return

    if user.id not in state.players:
        state.players[user.id] = Player(user.id, user.first_name)
        await query.answer(f"Welcome, {user.first_name}.")
        
        # Immediate UI Update (so you don't have to wait 5s for the name to appear)
        names = [p.name for p in state.players.values()]
        time_left = engine.get_time_left()
        
        try:
            join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
            await query.edit_message_text(
                text=Narrator.opening(names, time_left),
                reply_markup=join_btn,
                parse_mode='Markdown'
            )
        except: pass
    else:
        await query.answer("You are already in.")

async def cb_handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    state, _ = find_session(user_id)
    if not state:
        try: await query.answer("Session expired.", show_alert=True)
        except: pass
        return
    
    if data.startswith("night:"):
        try:
            target = int(data.split(":")[1])
            state.record_night_action(user_id, target, "generic") 
            await query.edit_message_text("🌑 Choice locked.")
        except: pass
        
    elif data.startswith("vote:"):
        target = int(data.split(":")[1])
        state.votes[user_id] = target
        await query.answer("Vote cast.")
