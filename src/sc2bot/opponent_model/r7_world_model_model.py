"""R7 learned macro-advisor prediction wrapper."""

from __future__ import annotations

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.interface import OpponentPrediction
from sc2bot.opponent_model.r7_world_model_runtime import R7WorldModelRuntime

_EXECUTABLE_ACTIONS = (
    "add_production",
    "add_tech",
    "increase_production_tempo",
    "defensive_hold",
    "move_out_window_open",
    "delay_move_out",
)


class R7WorldModelOpponentModel:
    model_name = "r7_world_model_runtime_v0"

    def __init__(self, runtime_path: str, *, history_window: int = 3) -> None:
        self.runtime = R7WorldModelRuntime(runtime_path, history_window=history_window)

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        if state is None:
            state = GameState.empty()
        payload = self.runtime.predict(
            state,
            observation,
            executable_actions=_EXECUTABLE_ACTIONS,
        )
        return OpponentPrediction(
            model_name=str(payload["model_name"]),
            opening_type=str(payload["opening_type"]),
            rush_risk=float(payload["rush_risk"]),
            tech_risk=float(payload["tech_risk"]),
            enemy_army_estimate=str(payload["predicted_future_pressure"]),
            confidence=float(payload["confidence"]),
            prediction_mode="learned_world_model_advisor",
            signals=tuple(payload["signals"]),
            recommended_response_tags=tuple(payload["recommended_response_tags"]),
            recommended_macro_action=str(payload["recommended_macro_action"]),
            macro_action_scores=dict(payload["macro_action_scores"]),
            predicted_future_winner=str(payload["predicted_future_winner"]),
            predicted_future_pressure=str(payload["predicted_future_pressure"]),
        )
