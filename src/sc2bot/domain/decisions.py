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
    continue_scouting_gate_active: bool = False
    defensive_posture_gate_active: bool = False
    first_attack_timing_gate_active: bool = False
    bounded_production_tempo_gate_active: bool = False
    first_attack_delay_seconds: float = 0.0
    first_attack_army_buffer: int = 0
    production_tempo_gateway_delta: int = 0
    selected_macro_action: str = "none"
    macro_action_scores: dict[str, float] = field(default_factory=dict)
    belief_summary: dict[str, object] = field(default_factory=dict)

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
            "continue_scouting_gate_active": self.continue_scouting_gate_active,
            "defensive_posture_gate_active": self.defensive_posture_gate_active,
            "first_attack_timing_gate_active": self.first_attack_timing_gate_active,
            "bounded_production_tempo_gate_active": self.bounded_production_tempo_gate_active,
            "first_attack_delay_seconds": self.first_attack_delay_seconds,
            "first_attack_army_buffer": self.first_attack_army_buffer,
            "production_tempo_gateway_delta": self.production_tempo_gateway_delta,
            "selected_macro_action": self.selected_macro_action,
            "macro_action_scores": self.macro_action_scores,
            "belief_summary": self.belief_summary,
        }


@dataclass(frozen=True)
class TacticalPlan:
    name: str
    strategy: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    order: str = "army_rally"
    reason: str = "no_army_available"
    defend_reason: str | None = None
    attack_reason: str | None = None
    regroup_reason: str | None = None
    rally_eligible: bool = False
    order_prerequisites_met: bool = False
    execution_evidence: str = "planning_only"
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
            "defend_reason": self.defend_reason,
            "attack_reason": self.attack_reason,
            "regroup_reason": self.regroup_reason,
            "rally_eligible": self.rally_eligible,
            "order_prerequisites_met": self.order_prerequisites_met,
            "execution_evidence": self.execution_evidence,
            "rally_point": list(self.rally_point) if self.rally_point else None,
            "target_position": list(self.target_position)
            if self.target_position
            else None,
            "own_army_count": self.own_army_count,
            "visible_enemy_units_count": self.visible_enemy_units_count,
        }
