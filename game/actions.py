from collections import defaultdict


class NightResult:
    def __init__(self):
        self.kills = set()
        self.protected = set()
        self.observations = defaultdict(list)


def resolve_night_actions(players, night_actions):
    """
    players: dict[user_id -> Player]
    night_actions: dict[actor_id -> target_id]
    """

    result = NightResult()

    # Step 1: Protection (Doctor, etc.)
    for actor_id, target_id in night_actions.items():
        actor = players.get(actor_id)
        target = players.get(target_id)

        if not actor or not target or not actor.alive:
            continue

        if actor.role.can_protect:
            result.protected.add(target.user_id)

    # Step 2: Observation (Watcher, etc.)
    for actor_id, target_id in night_actions.items():
        actor = players.get(actor_id)
        target = players.get(target_id)

        if not actor or not target or not actor.alive:
            continue

        if actor.role.can_observe:
            result.observations[actor.user_id].append(target.user_id)

    # Step 3: Killing (Bound One, etc.)
    for actor_id, target_id in night_actions.items():
        actor = players.get(actor_id)
        target = players.get(target_id)

        if not actor or not target or not actor.alive:
            continue

        if actor.role.can_kill:
            if target.user_id not in result.protected:
                result.kills.add(target.user_id)

    return result
