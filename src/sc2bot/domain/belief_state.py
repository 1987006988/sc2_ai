"""Typed belief-state object for the single adaptive research feature."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BeliefState:
    belief_time: float = 0.0
    scout_freshness_seconds: float | None = None
    enemy_contact_known: bool = False
    enemy_expansion_seen: bool = False
    enemy_combat_seen: bool = False
    enemy_tech_signal_seen: bool = False
    known_enemy_start_location_available: bool = False
    own_army_ready: bool = False
    first_attack_currently_eligible: bool = False

    rush_risk: float = 0.0
    tech_risk: float = 0.0
    information_confidence: float = 0.0
    information_gap_high: bool = False
    defensive_bias_active: bool = False
    scout_continuation_recommended: bool = False
    first_attack_timing_bias: str = "none"

    model_name: str = "unknown"
    prediction_mode: str = "none"
    signal_summary: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "belief_time": self.belief_time,
            "scout_freshness_seconds": self.scout_freshness_seconds,
            "enemy_contact_known": self.enemy_contact_known,
            "enemy_expansion_seen": self.enemy_expansion_seen,
            "enemy_combat_seen": self.enemy_combat_seen,
            "enemy_tech_signal_seen": self.enemy_tech_signal_seen,
            "known_enemy_start_location_available": self.known_enemy_start_location_available,
            "own_army_ready": self.own_army_ready,
            "first_attack_currently_eligible": self.first_attack_currently_eligible,
            "rush_risk": self.rush_risk,
            "tech_risk": self.tech_risk,
            "information_confidence": self.information_confidence,
            "information_gap_high": self.information_gap_high,
            "defensive_bias_active": self.defensive_bias_active,
            "scout_continuation_recommended": self.scout_continuation_recommended,
            "first_attack_timing_bias": self.first_attack_timing_bias,
            "model_name": self.model_name,
            "prediction_mode": self.prediction_mode,
            "signal_summary": list(self.signal_summary),
        }
