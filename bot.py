import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN

# Import all handlers from your UI file
from telegram_ui.handlers import (
    cmd_start_game, 
    cmd_kill_game, 
    cmd_force_start, 
    cmd_players, 
    cmd_extend, 
    cmd_role,
    cmd_help,
    cb_join, 
    cb_handle_input
)

# Enable logging so you can see errors in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

if __name__ == '__main__':
    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # --- COMMANDS ---
    # Core Game Lifecycle
    app.add_handler(CommandHandler('startgame', cmd_start_game))
    app.add_handler(CommandHandler('killgame', cmd_kill_game))   # Fixes stuck games
    app.add_handler(CommandHandler('forcestart', cmd_force_start))
    app.add_handler(CommandHandler('extend', cmd_extend))
    
    # Info & Status
    app.add_handler(CommandHandler('players', cmd_players))
    app.add_handler(CommandHandler('role', cmd_role))            # Resends role info
    app.add_handler(CommandHandler('help', cmd_help))            # Explains current phase
    
    # --- BUTTONS ---
    # Handles the "Join" button specifically
    app.add_handler(CallbackQueryHandler(cb_join, pattern="^join$"))
    
    # Handles all other game buttons (Voting, Night Actions)
    app.add_handler(CallbackQueryHandler(cb_handle_input))
    
    print("Veil Town is listening...")
    app.run_polling()
    
