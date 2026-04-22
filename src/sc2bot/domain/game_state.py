"""Game-state abstractions used by managers."""

from __future__ import annotations

from dataclasses import dataclass, field

Position = tuple[float, float]


@dataclass(frozen=True)
class GameState:
    game_loop: int
    game_time: float = 0.0
    own_race: str = "unknown"
    enemy_race: str = "unknown"
    own_start_location: Position | None = None
    known_enemy_start_location: Position | None = None
    visible_enemy_units_count: int = 0
    visible_enemy_structures_count: int = 0
    visible_enemy_units: tuple[str, ...] = field(default_factory=tuple)
    visible_enemy_structures: tuple[str, ...] = field(default_factory=tuple)
    visible_enemy_townhalls_count: int = 0
    own_workers_count: int = 0
    own_army_count: int = 0
    own_townhalls_count: int = 0
    minerals: int = 0
    vespene: int = 0
    supply_used: int = 0
    supply_cap: int = 0

    @classmethod
    def empty(cls) -> "GameState":
        return cls(game_loop=0)

    def to_dict(self) -> dict[str, object]:
        return {
            "game_loop": self.game_loop,
            "game_time": self.game_time,
            "own_race": self.own_race,
            "enemy_race": self.enemy_race,
            "own_start_location": list(self.own_start_location)
            if self.own_start_location
            else None,
            "known_enemy_start_location": list(self.known_enemy_start_location)
            if self.known_enemy_start_location
            else None,
            "visible_enemy_units_count": self.visible_enemy_units_count,
            "visible_enemy_structures_count": self.visible_enemy_structures_count,
            "visible_enemy_units": list(self.visible_enemy_units),
            "visible_enemy_structures": list(self.visible_enemy_structures),
            "visible_enemy_townhalls_count": self.visible_enemy_townhalls_count,
            "own_workers_count": self.own_workers_count,
            "own_army_count": self.own_army_count,
            "own_townhalls_count": self.own_townhalls_count,
            "minerals": self.minerals,
            "vespene": self.vespene,
            "supply_used": self.supply_used,
            "supply_cap": self.supply_cap,
        }
