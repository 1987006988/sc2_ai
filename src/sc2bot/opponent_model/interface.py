"""Stable opponent model interface for mainline code."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation


@dataclass(frozen=True)
class OpponentPrediction:
    model_name: str
    opening_type: str = "unknown"
    rush_risk: float = 0.0
    tech_risk: float = 0.0
    enemy_army_estimate: str = "unknown"
    confidence: float = 0.0
    prediction_mode: str = "prediction_only"
    signals: tuple[str, ...] = ()
    recommended_response_tags: tuple[str, ...] = ()
    recommended_macro_action: str = "none"
    macro_action_scores: dict[str, float] = field(default_factory=dict)
    predicted_future_winner: str = "unknown"
    predicted_future_pressure: str = "unknown"

    def to_dict(self) -> dict[str, object]:
        return {
            "model_name": self.model_name,
            "opening_type": self.opening_type,
            "rush_risk": self.rush_risk,
            "tech_risk": self.tech_risk,
            "enemy_army_estimate": self.enemy_army_estimate,
            "confidence": self.confidence,
            "prediction_mode": self.prediction_mode,
            "signals": list(self.signals),
            "recommended_response_tags": list(self.recommended_response_tags),
            "recommended_macro_action": self.recommended_macro_action,
            "macro_action_scores": self.macro_action_scores,
            "predicted_future_winner": self.predicted_future_winner,
            "predicted_future_pressure": self.predicted_future_pressure,
        }


class OpponentModel(Protocol):
    """Protocol implemented by all production opponent models."""

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        """Return a belief-state prediction from current scouting information."""
