# telegram_ui/buttons.py
# Inline keyboard builders for Veil Town

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def join_lobby_button():
    keyboard = [
        [InlineKeyboardButton("🕯️ Join Game", callback_data="join_game")]
    ]
    return InlineKeyboardMarkup(keyboard)


def extend_lobby_button():
    keyboard = [
        [InlineKeyboardButton("⏳ Extend Lobby", callback_data="extend_lobby")]
    ]
    return InlineKeyboardMarkup(keyboard)


def force_start_button():
    keyboard = [
        [InlineKeyboardButton("⚠️ Force Start", callback_data="force_start")]
    ]
    return InlineKeyboardMarkup(keyboard)


def vote_buttons(players):
    keyboard = []
    for p in players:
        keyboard.append(
            [InlineKeyboardButton(p.name, callback_data=f"vote:{p.user_id}")]
        )
    return InlineKeyboardMarkup(keyboard)


def night_action_buttons(players):
    keyboard = []
    for p in players:
        keyboard.append(
            [InlineKeyboardButton(p.name, callback_data=f"target:{p.user_id}")]
        )
    return InlineKeyboardMarkup(keyboard)
