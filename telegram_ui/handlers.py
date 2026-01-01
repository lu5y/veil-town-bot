from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from game.models import GameState, Player
from core.game_engine import GameEngine, Phase  # Added Phase import
from core.notifier import Notifier

SESSIONS = {}

async def cmd_start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # --- NEW RESTART LOGIC ---
    if chat_id in SESSIONS:
        state, engine = SESSIONS[chat_id]
        # If the game is NOT over, ignore the command (don't interrupt)
        if engine.phase != Phase.GAME_OVER:
            return 
        # If game IS over, we proceed and overwrite the old session
    # -------------------------
    
    state = GameState(chat_id)
    notifier = Notifier(context.bot, chat_id)
    engine = GameEngine(state, notifier)
    SESSIONS[chat_id] = (state, engine)
    
    join_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Join Veil Town", callback_data="join")]])
    await context.bot.send_message(chat_id, "Type /join or click below.", reply_markup=join_btn)
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
    alive = [p.name for p in state.players.values() if p.is_alive]
    
    msg = "**The Living:**\n" + "\n".join(alive) if alive else "None."
    await context.bot.send_message(chat_id, msg, parse_mode='Markdown')

async def cmd_extend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in SESSIONS: return
    
    await context.bot.send_message(chat_id, "⏳ Time extended.")

async def cb_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_chat.id
    user = query.from_user
    
    if chat_id not in SESSIONS: return
    state, engine = SESSIONS[chat_id]
    
    # Prevent joining if game is already running (not in Lobby)
    if engine.phase != Phase.LOBBY:
        return

    if user.id not in state.players:
        state.players[user.id] = Player(user.id, user.first_name)
        await context.bot.send_message(chat_id, f"{user.first_name} enters.")

async def cb_handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    
    # Locate session (User might be in DM)
    session = None
    for s_state, s_engine in SESSIONS.values():
        if user_id in s_state.players:
            session = (s_state, s_engine)
            break
            
    if not session: return
    state, engine = session
    
    if data.startswith("night:"):
        target = int(data.split(":")[1])
        state.record_night_action(user_id, target, "generic") 
        await query.edit_message_text("Action recorded.")
        
    elif data.startswith("vote:"):
        target = int(data.split(":")[1])
        state.votes[user_id] = target
    
