from dataclasses import dataclass, field
from enum import Enum, auto

class Phase(Enum):
    LOBBY = auto()
    DISCUSSION = auto()
    NIGHT = auto()
    RESOLUTION = auto()

@dataclass
class Player:
    user_id: int
    name: str
    role: str | None = None
    spoke: bool = False

@dataclass
class GameState:
    phase: Phase = Phase.LOBBY
    started: bool = False
    players: dict[int, Player] = field(default_factory=dict)
