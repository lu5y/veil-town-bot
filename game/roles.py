from enum import Enum

class Faction(Enum):
    TOWN = "Town"
    VEIL = "Veil"
    OUTSIDER = "Outsider"
    META = "Meta"

class RoleData:
    def __init__(self, name, faction, description, win_condition, has_night_action=False):
        self.name = name
        self.faction = faction
        self.description = description
        self.win_condition = win_condition
        self.has_night_action = has_night_action

# The Roster
ROLES = {
    # TOWN
    "Citizen": RoleData("Citizen", Faction.TOWN, "You have a vote. Use it.", "Eliminate the Veil.", False),
    "Watcher": RoleData("Watcher", Faction.TOWN, "You see movement in the dark. Learn if a player acted.", "Town survives.", True),
    "Archivist": RoleData("Archivist", Faction.TOWN, "History holds clues. Learn hidden details of past events.", "Town survives.", True),
    "Guardian": RoleData("Guardian", Faction.TOWN, "Protect one player. If unused, you are marked.", "Town survives.", True),
    
    # VEIL
    "Shade": RoleData("Shade", Faction.VEIL, "Eliminate one player. Cannot kill consecutively.", "Veil dominates.", True),
    "Whisperer": RoleData("Whisperer", Faction.VEIL, "Send a false system whisper to a player.", "Veil dominates.", True),
    "Mute": RoleData("Mute", Faction.VEIL, "Gains power in silence. Can block a vote.", "Veil dominates.", True),

    # OUTSIDERS
    "Stranger": RoleData("Stranger", Faction.OUTSIDER, "Unlock power if targeted twice.", "Survive until 3 remain.", False),
    "Confessor": RoleData("Confessor", Faction.OUTSIDER, "Learn a secret.", "Reveal role publicly and survive one day.", True),
    "Judge": RoleData("Judge", Faction.OUTSIDER, "Breaks tied votes.", "Survive to the end.", False),

    # META
    "Omen": RoleData("Omen", Faction.META, "Escalates darkness. After 3 nights, roles are hidden on death.", "Always wins.", False),
    "Last Light": RoleData("Last Light", Faction.META, "Raises execution threshold.", "Town survives.", False),
}
