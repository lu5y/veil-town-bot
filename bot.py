import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from telegram_ui.handlers import cmd_start_game, cb_join, cb_handle_input

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# In bot.py

# ... imports ...

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # --- COMMANDS ---
    app.add_handler(CommandHandler('startgame', cmd_start_game))
    app.add_handler(CommandHandler('forcestart', cmd_force_start)) # Ensure you add this function to handlers.py
    app.add_handler(CommandHandler('players', cmd_players))        # Ensure you add this function to handlers.py
    
    # --- BUTTONS ---
    app.add_handler(CallbackQueryHandler(cb_join, pattern="^join$"))
    app.add_handler(CallbackQueryHandler(cb_handle_input))
    
    print("Veil Town is listening...")
    app.run_polling()
