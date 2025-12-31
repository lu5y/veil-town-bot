from dataclasses import dataclass, field

@dataclass
class Player:
    user_id: int
    name: str
    role: str | None = None
    spoke: bool = False

@dataclass
class GameState:
    started: bool = False
    phase: str = "LOBBY"  # LOBBY | DISCUSSION
    players: dict[int, Player] = field(default_factory=dict)
