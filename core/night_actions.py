from game.models import GameState


class NightActionHandler:
    @staticmethod
    async def handle(game: GameState, user_id: int, target_id: int):
        actor = game.players.get(user_id)
        target = game.players.get(target_id)

        if not actor or not target or not target.alive:
            return "Nothing happens."

        if actor.role == "Doctor":
            game.night_actions.protected = target_id
            return f"You tended to {target.name}."

        if actor.role == "Watcher":
            game.night_actions.watched[user_id] = target_id
            return f"You observed {target.name}."

        if actor.role == "Bound One":
            game.night_actions.marked = target_id
            return f"You followed the compulsion."

        return "You have no influence tonight."
