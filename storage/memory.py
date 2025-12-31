# storage/memory.py
# Central in-memory storage for all active game sessions

from typing import Dict, Optional


class MemoryStore:
    """
    Stores all active game sessions by chat_id.
    This is the single source of truth for running games.
    """

    def __init__(self):
        self.sessions: Dict[int, dict] = {}

    # ----------------------------
    # SESSION MANAGEMENT
    # ----------------------------

    def create_session(self, chat_id: int, session_data: dict):
        self.sessions[chat_id] = session_data

    def get_session(self, chat_id: int) -> Optional[dict]:
        return self.sessions.get(chat_id)

    def has_session(self, chat_id: int) -> bool:
        return chat_id in self.sessions

    def remove_session(self, chat_id: int):
        if chat_id in self.sessions:
            del self.sessions[chat_id]

    # ----------------------------
    # PLAYER HELPERS
    # ----------------------------

    def add_player(self, chat_id: int, user_id: int, player):
        session = self.get_session(chat_id)
        if not session:
            return
        session["players"][user_id] = player

    def get_players(self, chat_id: int):
        session = self.get_session(chat_id)
        if not session:
            return {}
        return session.get("players", {})

    # ----------------------------
    # STATE FLAGS
    # ----------------------------

    def set_flag(self, chat_id: int, key: str, value):
        session = self.get_session(chat_id)
        if not session:
            return
        session[key] = value

    def get_flag(self, chat_id: int, key: str, default=None):
        session = self.get_session(chat_id)
        if not session:
            return default
        return session.get(key, default)


# Global singleton (intentionally)
MEMORY = MemoryStore()
