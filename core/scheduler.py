import random
from game.whispers import WHISPERS


class NightScheduler:
    @staticmethod
    async def run_night(game, bot):
        players = list(game.players.values())

        if not players:
            return

        # Select roughly half the players (minimum 1)
        count = max(1, len(players) // 2)
        targets = random.sample(players, count)

        for player in targets:
            whisper = random.choice(WHISPERS)
            await bot.send_message(
                chat_id=player.user_id,
                text=whisper
            )
