from game.models import GameState


class ConsequenceResolver:
    @staticmethod
    def resolve(game: GameState):
        marked = game.night_actions.marked
        protected = game.night_actions.protected

        # No mark → nothing happens
        if not marked:
            return None

        # Protection prevents death
        if marked == protected:
            return None

        victim = game.players.get(marked)
        if not victim or not victim.alive:
            return None

        victim.alive = False
        return victim
