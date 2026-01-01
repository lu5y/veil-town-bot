# ... imports ...
from telegram_ui.handlers import (
    cmd_start_game, 
    cmd_kill_game,  # <--- NEW IMPORT
    cmd_force_start, 
    cmd_players, 
    cmd_extend, 
    cmd_role,
    cmd_help,
    cb_join, 
    cb_handle_input
)

if __name__ == '__main__':
    # ... setup ...
    
    app.add_handler(CommandHandler('startgame', cmd_start_game))
    app.add_handler(CommandHandler('killgame', cmd_kill_game)) # <--- NEW HANDLER
    app.add_handler(CommandHandler('forcestart', cmd_force_start))
    # ... rest of handlers ...
    
