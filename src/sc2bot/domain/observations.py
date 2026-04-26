"""Observation structures for scouting and opponent modeling."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoutingObservation:
    game_loop: int
    game_time: float = 0.0
    current_enemy_units: tuple[str, ...] = field(default_factory=tuple)
    current_enemy_structures: tuple[str, ...] = field(default_factory=tuple)
    current_enemy_combat_units: tuple[str, ...] = field(default_factory=tuple)
    enemy_units_seen: tuple[str, ...] = field(default_factory=tuple)
    enemy_structures_seen: tuple[str, ...] = field(default_factory=tuple)
    enemy_expansions_seen: int = 0
    first_enemy_seen_time: float | None = None
    last_enemy_seen_time: float | None = None
    seen_enemy_structures: tuple[str, ...] = field(default_factory=tuple)
    seen_enemy_combat_units: tuple[str, ...] = field(default_factory=tuple)
    enemy_expansion_seen: bool = False
    possible_tech_signal: bool = False
    possible_rush_signal: bool = False
    observation_confidence: float = 0.0

    @classmethod
    def empty(cls, game_loop: int = 0) -> "ScoutingObservation":
        return cls(game_loop=game_loop)

    def to_dict(self) -> dict[str, object]:
        return {
            "game_loop": self.game_loop,
            "game_time": self.game_time,
            "current_enemy_units": list(self.current_enemy_units),
            "current_enemy_structures": list(self.current_enemy_structures),
            "current_enemy_combat_units": list(self.current_enemy_combat_units),
            "enemy_units_seen": list(self.enemy_units_seen),
            "enemy_structures_seen": list(self.enemy_structures_seen),
            "enemy_expansions_seen": self.enemy_expansions_seen,
            "first_enemy_seen_time": self.first_enemy_seen_time,
            "last_enemy_seen_time": self.last_enemy_seen_time,
            "seen_enemy_structures": list(self.seen_enemy_structures),
            "seen_enemy_combat_units": list(self.seen_enemy_combat_units),
            "enemy_expansion_seen": self.enemy_expansion_seen,
            "possible_tech_signal": self.possible_tech_signal,
            "possible_rush_signal": self.possible_rush_signal,
            "observation_confidence": self.observation_confidence,
        }
