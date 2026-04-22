"""Decision dataclasses emitted by managers."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StrategyDecision:
    name: str
    tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class StrategyResponse:
    selected_response_tag: str = "none"
    strategy_switch_reason: str = "none"
    intervention_mode: str = "none"
    opponent_model_mode: str = "unknown"
    prediction_model_name: str = "unknown"
    prediction_mode: str = "none"
    prediction_opening_type: str = "unknown"
    rush_risk: float = 0.0
    tech_risk: float = 0.0
    confidence: float = 0.0
    prediction_signals: tuple[str, ...] = field(default_factory=tuple)
    recommended_response_tags: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "selected_response_tag": self.selected_response_tag,
            "strategy_switch_reason": self.strategy_switch_reason,
            "intervention_mode": self.intervention_mode,
            "opponent_model_mode": self.opponent_model_mode,
            "prediction_model_name": self.prediction_model_name,
            "prediction_mode": self.prediction_mode,
            "prediction_opening_type": self.prediction_opening_type,
            "rush_risk": self.rush_risk,
            "tech_risk": self.tech_risk,
            "confidence": self.confidence,
            "prediction_signals": list(self.prediction_signals),
            "recommended_response_tags": list(self.recommended_response_tags),
        }


@dataclass(frozen=True)
class TacticalPlan:
    name: str
    strategy: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    order: str = "army_rally"
    reason: str = "no_army_available"
    rally_point: tuple[float, float] | None = None
    target_position: tuple[float, float] | None = None
    own_army_count: int = 0
    visible_enemy_units_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "strategy": self.strategy,
            "tags": list(self.tags),
            "order": self.order,
            "reason": self.reason,
            "rally_point": list(self.rally_point) if self.rally_point else None,
            "target_position": list(self.target_position)
            if self.target_position
            else None,
            "own_army_count": self.own_army_count,
            "visible_enemy_units_count": self.visible_enemy_units_count,
        }
