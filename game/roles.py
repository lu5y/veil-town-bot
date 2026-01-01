from enum import Enum, auto

class Faction(Enum):
    TOWN = auto()
    VEIL = auto()
    OUTSIDER = auto()

class Role:
    def __init__(self, name, faction, description, win_condition, has_night_action=False):
        self.name = name
        self.faction = faction
        self.description = description
        self.win_condition = win_condition
        self.has_night_action = has_night_action

# FULL ROSTER RESTORED
ROLES = {
    "Shade": Role("Shade", Faction.VEIL, "Eliminate one player each night.", "Veil dominates.", True),
    "Whisperer": Role("Whisperer", Faction.VEIL, "Confuse the town with lies.", "Veil dominates.", True),
    "Mute": Role("Mute", Faction.VEIL, "Silence a player during the day.", "Veil dominates.", True),
    
    "Watcher": Role("Watcher", Faction.TOWN, "Learn if a player acted at night.", "Town survives.", True),
    "Guardian": Role("Guardian", Faction.TOWN, "Protect one player from death.", "Town survives.", True),
    "Archivist": Role("Archivist", Faction.TOWN, "Learn the history of the town.", "Town survives.", True),
    "Citizen": Role("Citizen", Faction.TOWN, "Vote to save the town.", "Town survives.", False),
    
    "Stranger": Role("Stranger", Faction.OUTSIDER, "You must be targeted to win.", "Be targeted.", False),
    "Confessor": Role("Confessor", Faction.OUTSIDER, "Reveal one player's role once.", " Survive.", True),
    "Judge": Role("Judge", Faction.OUTSIDER, "Your vote counts double.", "Town survives.", False),
    
    "Omen": Role("Omen", Faction.OUTSIDER, "If you die, the killer dies too.", "Die at night.", False),
    "Last Light": Role("Last Light", Faction.OUTSIDER, "If you die, night is eternal.", "Survive.", False)
}
