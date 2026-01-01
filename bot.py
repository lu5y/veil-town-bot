import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN

# This block imports ALL the functions you just added to handlers.py
from telegram_ui.handlers import (
    cmd_start_game, 
    cmd_force_start, 
    cmd_players, 
    cmd_extend, 
    cb_join, 
    cb_handle_input
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Group Commands
    app.add_handler(CommandHandler('startgame', cmd_start_game))
    app.add_handler(CommandHandler('forcestart', cmd_force_start))
    app.add_handler(CommandHandler('players', cmd_players))
    app.add_handler(CommandHandler('extend', cmd_extend))
    
    # Universal Callback Handler (Joins, Night Actions, Votes)
    app.add_handler(CallbackQueryHandler(cb_join, pattern="^join$"))
    app.add_handler(CallbackQueryHandler(cb_handle_input))
    
    print("Veil Town is listening...")
    app.run_polling()
