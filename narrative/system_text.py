# narrative/system_text.py
# Centralized system and phase text for Veil Town

# ----------------------------
# START MESSAGES
# ----------------------------

START_PRIVATE = (
    "🕯️ **Veil Town**\n\n"
    "A hidden-role horror game of whispers, deception, and judgment.\n\n"
    "• Join games in group chats\n"
    "• Receive your role in private\n"
    "• Make silent choices through buttons\n"
    "• Face public consequences\n\n"
    "Add me to a group to begin."
)

START_GROUP = (
    "🕯️ **Veil Town** is here.\n\n"
    "A game of secrets and survival.\n"
    "Use /startgame to open a lobby."
)

# ----------------------------
# LOBBY
# ----------------------------

LOBBY_OPEN = (
    "🕯️ **Lobby Open**\n\n"
    "Players may now join the game.\n"
    "The game will begin automatically once enough players join."
)

LOBBY_EXTENDED = (
    "⏳ **Lobby Extended**\n\n"
    "Waiting a little longer for more players to arrive."
)

NOT_ENOUGH_PLAYERS = (
    "❗ The ritual fails.\n\n"
    "Not enough players joined the game."
)

GAME_STARTING = (
    "🕯️ **The game is beginning…**\n\n"
    "Roles are being assigned.\n"
    "Check your private messages."
)

# ----------------------------
# PHASE TEXT
# ----------------------------

PHASE_NIGHT = (
    "🌑 **Night falls over Veil Town.**\n\n"
    "Those with secret actions may now act.\n"
    "The town sleeps… but not everyone."
)

PHASE_DAY = (
    "🌕 **Day breaks.**\n\n"
    "Whispers spread.\n"
    "The town discusses what happened in the dark."
)

PHASE_JUDGMENT = (
    "⚖️ **Judgment Phase**\n\n"
    "Cast your vote.\n"
    "Silence is a choice — and it has consequences."
)

# ----------------------------
# END GAME
# ----------------------------

GAME_OVER = (
    "🕯️ **The veil has lifted.**\n\n"
    "The game is over."
)

# ----------------------------
# GENERIC ERRORS
# ----------------------------

ERROR_GAME_RUNNING = (
    "❗ A game is already running in this group."
)

ERROR_NO_GAME = (
    "❗ No active game in this group."
)
