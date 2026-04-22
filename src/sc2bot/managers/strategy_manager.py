"""Strategy manager skeleton."""

from sc2bot.config.schema import OpponentModelConfig
from sc2bot.domain.decisions import StrategyDecision, StrategyResponse
from sc2bot.domain.game_state import GameState
from sc2bot.opponent_model.interface import OpponentPrediction


class StrategyManager:
    """Selects the high-level game plan."""

    def decide(self, state: GameState, prediction: OpponentPrediction) -> StrategyDecision:
        _ = state
        return StrategyDecision(
            name="hold_default_plan",
            tags=("safe", prediction.prediction_mode, *prediction.recommended_response_tags),
        )

    def select_response(
        self,
        prediction: OpponentPrediction,
        config: OpponentModelConfig,
    ) -> StrategyResponse:
        """Select a telemetry-only strategy response tag from one prediction."""

        if config.intervention_mode not in {"tag_only", "minimal_behavior"}:
            return _response_from_prediction(
                prediction,
                config,
                selected_response_tag="none",
                strategy_switch_reason="none",
            )

        if prediction.rush_risk >= config.rush_risk_threshold:
            return _response_from_prediction(
                prediction,
                config,
                selected_response_tag="defensive_posture",
                strategy_switch_reason="rush_risk_high",
            )
        if prediction.tech_risk >= config.tech_risk_threshold:
            return _response_from_prediction(
                prediction,
                config,
                selected_response_tag="tech_alert",
                strategy_switch_reason="tech_risk_high",
            )
        if prediction.confidence <= config.low_information_confidence_threshold:
            return _response_from_prediction(
                prediction,
                config,
                selected_response_tag="continue_scouting",
                strategy_switch_reason="low_information",
            )
        return _response_from_prediction(
            prediction,
            config,
            selected_response_tag="none",
            strategy_switch_reason="none",
        )


def _response_from_prediction(
    prediction: OpponentPrediction,
    config: OpponentModelConfig,
    *,
    selected_response_tag: str,
    strategy_switch_reason: str,
) -> StrategyResponse:
    return StrategyResponse(
        selected_response_tag=selected_response_tag,
        strategy_switch_reason=strategy_switch_reason,
        intervention_mode=config.intervention_mode,
        opponent_model_mode=config.mode,
        prediction_model_name=prediction.model_name,
        prediction_mode=prediction.prediction_mode,
        prediction_opening_type=prediction.opening_type,
        rush_risk=prediction.rush_risk,
        tech_risk=prediction.tech_risk,
        confidence=prediction.confidence,
        prediction_signals=prediction.signals,
        recommended_response_tags=prediction.recommended_response_tags,
    )
