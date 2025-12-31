from enum import Enum, auto
from collections import defaultdict, Counter
import random


# ----------------------------
# PHASE ENUM (ENGINE USES THIS)
# ----------------------------
class Phase(Enum):
    WAITING = auto()
    RUNNING = auto()
    ENDED = auto()


# ----------------------------
# PLAYER
# ----------------------------
class Player:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.role = None
        self.alive = True

        # tracking
        self.missed_actions = 0
        self.missed_votes = 0


# ----------------------------
# GAME STATE (TRUTH)
# ----------------------------
class GameState:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

        self.players: dict[int, Player] = {}
        self.phase = Phase.WAITING

        # night
        self.night_actions = {}      # actor_id -> target_id
        self.last_night_deaths = []

        # voting
        self.votes = {}              # voter_id -> target_id

        # flags
        self.started = False

    # ----------------------------
    # PLAYER HELPERS
    # ----------------------------
    def alive_players(self):
        return [p for p in self.players.values() if p.alive]

    def dead_players(self):
        return [p for p in self.players.values() if not p.alive]

    def get_player(self, user_id):
        return self.players.get(user_id)

    # ----------------------------
    # ROLE ASSIGNMENT
    # ----------------------------
    def assign_roles(self, roles):
        shuffled_roles = roles[:]
        random.shuffle(shuffled_roles)

        for player, role in zip(self.players.values(), shuffled_roles):
            player.role = role

        self.started = True

    # ----------------------------
    # NIGHT ACTIONS
    # ----------------------------
    def record_night_action(self, actor_id, target_id):
        self.night_actions[actor_id] = target_id

    def resolve_night(self):
        """
        Very simple resolution for now.
        Later, actions.py will expand this.
        """
        self.last_night_deaths.clear()

        kill_targets = []

        for actor_id, target_id in self.night_actions.items():
            actor = self.players.get(actor_id)
            target = self.players.get(target_id)

            if not actor or not target:
                continue

            if actor.role.can_kill:
                kill_targets.append(target)

        # Apply deaths (no protection yet)
        for victim in kill_targets:
            if victim.alive:
                victim.alive = False
                self.last_night_deaths.append(victim)

        self.night_actions.clear()
        return self.last_night_deaths

    def last_night_deaths(self):
        return self.last_night_deaths

    # ----------------------------
    # VOTING
    # ----------------------------
    def record_vote(self, voter_id, target_id):
        self.votes[voter_id] = target_id

    def resolve_votes(self):
        if not self.votes:
            return None

        counter = Counter(self.votes.values())
        target_id, _ = counter.most_common(1)[0]

        target = self.players.get(target_id)
        if target and target.alive:
            target.alive = False

        self.votes.clear()
        return target

    # ----------------------------
    # WIN CONDITIONS
    # ----------------------------
    def check_win(self):
        alive = self.alive_players()
        return len(alive) <= 2

    def endgame_summary(self):
        alive = self.alive_players()
        dead = self.dead_players()

        text = "🩸 **The Veil Lifts.**\n\n"

        if alive:
            text += "**Alive:**\n"
            for p in alive:
                text += f"– {p.name}\n"

        if dead:
            text += "\n**Dead:**\n"
            for p in dead:
                text += f"– {p.name}\n"

        text += "\nThe town does not recover."

        return text

    # ----------------------------
    # RESET
    # ----------------------------
    def reset(self):
        self.players.clear()
        self.night_actions.clear()
        self.votes.clear()
        self.last_night_deaths.clear()
        self.phase = Phase.WAITING
        self.started = False
