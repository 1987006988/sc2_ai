"""Rule-based R7 macro-advisor comparator."""

from __future__ import annotations

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.interface import OpponentPrediction


class R7RuleMacroAdvisorOpponentModel:
    model_name = "r7_rule_macro_advisor"

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        state = state or GameState.empty()
        if observation.possible_rush_signal or state.visible_enemy_units_count > 0:
            action = "defensive_hold"
            rush_risk = 0.7
            tech_risk = 0.2
        elif observation.possible_tech_signal:
            action = "add_tech"
            rush_risk = 0.25
            tech_risk = 0.65
        elif state.own_army_count < 4:
            action = "add_production"
            rush_risk = 0.25
            tech_risk = 0.2
        elif state.game_time >= 300.0 and state.own_army_count >= 8:
            action = "move_out_window_open"
            rush_risk = 0.15
            tech_risk = 0.2
        else:
            action = "delay_move_out"
            rush_risk = 0.2
            tech_risk = 0.2
        scores = {
            "add_production": 0.2,
            "add_tech": 0.2,
            "increase_production_tempo": 0.2,
            "defensive_hold": 0.2,
            "move_out_window_open": 0.2,
            "delay_move_out": 0.2,
        }
        scores[action] = 0.8
        return OpponentPrediction(
            model_name=self.model_name,
            opening_type="rule_based_macro",
            rush_risk=rush_risk,
            tech_risk=tech_risk,
            enemy_army_estimate="rule_proxy",
            confidence=0.55,
            prediction_mode="rule_macro_advisor",
            signals=(f"macro_action:{action}",),
            recommended_response_tags=("macro_advisor",),
            recommended_macro_action=action,
            macro_action_scores=scores,
            predicted_future_winner="unknown",
            predicted_future_pressure="high_pressure" if action == "defensive_hold" else "low_pressure",
        )
