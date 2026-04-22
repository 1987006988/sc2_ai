"""Scouting manager skeleton."""

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.telemetry.event_logger import EventLogger

_COMBAT_UNIT_HINTS = {
    "adept",
    "archon",
    "baneling",
    "battlecruiser",
    "carrier",
    "colossus",
    "cyclone",
    "darktemplar",
    "hellion",
    "hellbat",
    "hydralisk",
    "immortal",
    "liberator",
    "marine",
    "marauder",
    "medivac",
    "mutalisk",
    "oracle",
    "phoenix",
    "queen",
    "roach",
    "stalker",
    "tank",
    "tempest",
    "ultralisk",
    "voidray",
    "viking",
    "zealot",
    "zergling",
}

_TECH_STRUCTURE_HINTS = {
    "banelingnest",
    "barrackstechlab",
    "cyberneticscore",
    "darkshrine",
    "extractor",
    "factory",
    "fleetbeacon",
    "fusioncore",
    "ghostacademy",
    "lair",
    "lurkerdenmp",
    "nexus",
    "refinery",
    "roboticsbay",
    "roboticsfacility",
    "spire",
    "spawningpool",
    "stargate",
    "starport",
    "templararchive",
    "twilightcouncil",
}


class ScoutingManager:
    """Collects observations that feed strategy and opponent modeling."""

    def __init__(self, telemetry: EventLogger | None = None) -> None:
        self.telemetry = telemetry
        self._first_enemy_seen_time: float | None = None
        self._last_enemy_seen_time: float | None = None
        self._enemy_units_seen: set[str] = set()
        self._enemy_structures_seen: set[str] = set()
        self._enemy_combat_units_seen: set[str] = set()

    def update(self, state: GameState) -> ScoutingObservation:
        enemy_seen_now = bool(
            state.visible_enemy_units_count or state.visible_enemy_structures_count
        )
        if enemy_seen_now:
            if self._first_enemy_seen_time is None:
                self._first_enemy_seen_time = state.game_time
            self._last_enemy_seen_time = state.game_time
        self._enemy_units_seen.update(state.visible_enemy_units)
        self._enemy_structures_seen.update(state.visible_enemy_structures)
        self._enemy_combat_units_seen.update(
            unit
            for unit in state.visible_enemy_units
            if unit.lower().replace("_", "") in _COMBAT_UNIT_HINTS
        )
        possible_tech_signal = any(
            structure.lower().replace("_", "") in _TECH_STRUCTURE_HINTS
            for structure in self._enemy_structures_seen
        )
        possible_rush_signal = bool(
            self._enemy_combat_units_seen
            and self._first_enemy_seen_time is not None
            and self._first_enemy_seen_time <= 180.0
        )
        confidence = 0.0
        if self._enemy_units_seen or self._enemy_structures_seen:
            confidence = min(
                1.0, 0.2 + 0.05 * (len(self._enemy_units_seen) + len(self._enemy_structures_seen))
            )
        enemy_expansions_seen = max(0, state.visible_enemy_townhalls_count - 1)
        observation = ScoutingObservation(
            game_loop=state.game_loop,
            game_time=state.game_time,
            enemy_units_seen=tuple(sorted(self._enemy_units_seen)),
            enemy_structures_seen=tuple(sorted(self._enemy_structures_seen)),
            enemy_expansions_seen=enemy_expansions_seen,
            first_enemy_seen_time=self._first_enemy_seen_time,
            last_enemy_seen_time=self._last_enemy_seen_time,
            seen_enemy_structures=tuple(sorted(self._enemy_structures_seen)),
            seen_enemy_combat_units=tuple(sorted(self._enemy_combat_units_seen)),
            enemy_expansion_seen=enemy_expansions_seen > 0,
            possible_tech_signal=possible_tech_signal,
            possible_rush_signal=possible_rush_signal,
            observation_confidence=confidence,
        )
        if self.telemetry:
            self.telemetry.record("scouting_observation", observation.to_dict())
        return observation
