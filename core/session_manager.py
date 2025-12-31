from game.models import GameState


class SessionManager:
    def __init__(self):
        self.games = {}

    def get_game(self, chat_id: int) -> GameState:
        if chat_id not in self.games:
            self.games[chat_id] = GameState(chat_id)
        return self.games[chat_id]

    def end_game(self, chat_id: int):
        if chat_id in self.games:
            del self.games[chat_id]
