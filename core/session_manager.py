from game.models import GameState

class SessionManager:
    def __init__(self):
        self.games = {}

    def get_game(self, chat_id):
        if chat_id not in self.games:
            self.games[chat_id] = GameState()
        return self.games[chat_id]
