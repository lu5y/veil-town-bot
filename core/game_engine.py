# core/engine.py
# Central game engine for Veil Town (wiring version)

from narrative import announcements, whispers
from storage.memory import MEMORY


class GameEngine:
    def __init__(self, min_players=5, max_players=15):
        self.min_players = min_players
        self.max_players = max_players

    # ----------------------------
    # SESSION CHECKS
    # ----------------------------

    def has_game(self, chat_id: int) -> bool:
        return MEMORY.has_session(chat_id)

    # ----------------------------
    # GAME LIFECYCLE
    # ----------------------------

    def create_game(self, chat_id: int):
        session = {
            "players": {},
            "phase": "lobby",
            "extended": False,
        }
        MEMORY.create_session(chat_id, session)

    def add_player(self, chat_id: int, user):
        session = MEMORY.get_session(chat_id)
        if not session:
            return

        if len(session["players"]) >= self.max_players:
            return

        if user.id in session["players"]:
            return

        session["players"][user.id] = {
            "user": user,
            "alive": True,
        }

    def extend_lobby(self, chat_id: int):
        session = MEMORY.get_session(chat_id)
        if not session:
            return
        session["extended"] = True

    def force_start(self, chat_id: int):
        session = MEMORY.get_session(chat_id)
        if not session:
            return

        session["phase"] = "night"

    # ----------------------------
    # PHASE HANDLING
    # ----------------------------

    def announce_lobby_open(self):
        return announcements.announce_lobby_open()

    def announce_lobby_extended(self):
        return announcements.announce_lobby_extended()

    def announce_game_start(self):
        return announcements.announce_game_start()

    def announce_night(self):
        return announcements.announce_night()

    def announce_dawn(self):
        return announcements.announce_dawn(deaths=[])

    def announce_judgment(self):
        return announcements.announce_judgment()

    def announce_game_over(self, chat_id: int):
        session = MEMORY.get_session(chat_id)
        if not session:
            return announcements.announce_game_over([])

        alive = [
            p["user"]
            for p in session["players"].values()
            if p["alive"]
        ]
        return announcements.announce_game_over(alive)

    # ----------------------------
    # PRIVATE MESSAGES
    # ----------------------------

    def get_role_message(self, player):
        return whispers.role_reveal(player)

    def get_night_prompt(self, role_name):
        return whispers.night_action_prompt(role_name)

    def confirm_action(self):
        return whispers.action_confirmed()
