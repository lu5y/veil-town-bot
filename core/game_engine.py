# core/engine.py

class GameEngine:
    """
    Placeholder engine to keep the bot stable.
    Full phase automation will be added later.
    """

    def __init__(self):
        self.running = False

    def start_game(self, chat_id: int):
        self.running = True
        return f"Game started in chat {chat_id}"

    def stop_game(self, chat_id: int):
        self.running = False
        return f"Game stopped in chat {chat_id}"

    def tick(self):
        """
        Future hook for automatic phase transitions.
        Currently does nothing.
        """
        pass
