"""Strategy manager skeleton."""

from sc2bot.config.schema import OpponentModelConfig
from sc2bot.domain.belief_state import BeliefState
from sc2bot.domain.decisions import StrategyDecision, StrategyResponse
from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.interface import OpponentPrediction


class StrategyManager:
    """Selects the high-level game plan."""

    def decide(self, state: GameState, prediction: OpponentPrediction) -> StrategyDecision:
        _ = state
        return StrategyDecision(
            name="hold_default_plan",
            tags=(
                "safe",
                prediction.prediction_mode,
                prediction.recommended_macro_action,
                *prediction.recommended_response_tags,
            ),
        )

    def select_response(
        self,
        state: GameState,
        observation: ScoutingObservation,
        prediction: OpponentPrediction,
        config: OpponentModelConfig,
    ) -> StrategyResponse:
        """Select an auditable strategy response from state, scouting, and prediction."""

        belief = build_belief_state(
            state=state,
            observation=observation,
            prediction=prediction,
            config=config,
        )

        if config.intervention_mode == "macro_world_model_advisor":
            return _macro_world_model_response_from_prediction(prediction, config, belief)

        if config.intervention_mode == "adaptive_gating":
            return _adaptive_response_from_belief(prediction, config, belief)

        if config.intervention_mode not in {"tag_only", "minimal_behavior"}:
            return _response_from_prediction(
                prediction,
                config,
                belief=belief,
                selected_response_tag="none",
                strategy_switch_reason="none",
            )

        if prediction.rush_risk >= config.rush_risk_threshold:
            return _response_from_prediction(
                prediction,
                config,
                belief=belief,
                selected_response_tag="defensive_posture",
                strategy_switch_reason="rush_risk_high",
            )
        if prediction.tech_risk >= config.tech_risk_threshold:
            return _response_from_prediction(
                prediction,
                config,
                belief=belief,
                selected_response_tag="tech_alert",
                strategy_switch_reason="tech_risk_high",
            )
        if prediction.confidence <= config.low_information_confidence_threshold:
            return _response_from_prediction(
                prediction,
                config,
                belief=belief,
                selected_response_tag="continue_scouting",
                strategy_switch_reason="low_information",
            )
        return _response_from_prediction(
            prediction,
            config,
            belief=belief,
            selected_response_tag="none",
            strategy_switch_reason="none",
        )


def build_belief_state(
    *,
    state: GameState,
    observation: ScoutingObservation,
    prediction: OpponentPrediction,
    config: OpponentModelConfig,
) -> BeliefState:
    scout_freshness_seconds: float | None
    if observation.last_enemy_seen_time is None:
        scout_freshness_seconds = None
    else:
        scout_freshness_seconds = max(0.0, state.game_time - observation.last_enemy_seen_time)
    enemy_contact_known = bool(
        observation.enemy_units_seen or observation.enemy_structures_seen
    )
    learned_temporal_mode = prediction.prediction_mode == "learned_temporal_belief"
    if learned_temporal_mode:
        # For the learned treatment, low confidence alone should not keep the
        # response surface latched on after we have already made contact.
        information_gap_high = (
            (
                prediction.confidence <= config.low_information_confidence_threshold
                and not enemy_contact_known
            )
            or (
                not enemy_contact_known
                and state.game_time >= config.low_information_game_time_threshold
            )
        )
    else:
        information_gap_high = (
            prediction.confidence <= config.low_information_confidence_threshold
            or (
                not enemy_contact_known
                and state.game_time >= config.low_information_game_time_threshold
            )
        )
    defensive_bias_active = prediction.rush_risk >= config.rush_risk_threshold
    scout_continuation_recommended = (
        state.game_time <= config.scout_continuation_game_time_limit
        and (
            information_gap_high
            or not enemy_contact_known
            or scout_freshness_seconds is None
            or scout_freshness_seconds >= 30.0
        )
    )
    if defensive_bias_active:
        first_attack_timing_bias = "rush_risk_delay"
    elif information_gap_high:
        first_attack_timing_bias = "information_gap_delay"
    else:
        first_attack_timing_bias = "none"
    return BeliefState(
        belief_time=state.game_time,
        scout_freshness_seconds=scout_freshness_seconds,
        enemy_contact_known=enemy_contact_known,
        enemy_expansion_seen=observation.enemy_expansion_seen,
        enemy_combat_seen=bool(observation.seen_enemy_combat_units),
        enemy_tech_signal_seen=observation.possible_tech_signal,
        known_enemy_start_location_available=state.known_enemy_start_location is not None,
        own_army_ready=state.own_army_count > 0,
        first_attack_currently_eligible=(
            state.known_enemy_start_location is not None and state.own_army_count > 0
        ),
        rush_risk=prediction.rush_risk,
        tech_risk=prediction.tech_risk,
        information_confidence=prediction.confidence,
        information_gap_high=information_gap_high,
        defensive_bias_active=defensive_bias_active,
        scout_continuation_recommended=scout_continuation_recommended,
        first_attack_timing_bias=first_attack_timing_bias,
        model_name=prediction.model_name,
        prediction_mode=prediction.prediction_mode,
        signal_summary=prediction.signals,
    )


def _response_from_prediction(
    prediction: OpponentPrediction,
    config: OpponentModelConfig,
    *,
    belief: BeliefState,
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
        belief_summary=belief.to_dict(),
    )


def _adaptive_response_from_belief(
    prediction: OpponentPrediction,
    config: OpponentModelConfig,
    belief: BeliefState,
) -> StrategyResponse:
    continue_scouting_gate_active = belief.scout_continuation_recommended
    defensive_posture_gate_active = belief.defensive_bias_active
    first_attack_timing_gate_active = belief.first_attack_timing_bias != "none"
    learned_temporal_mode = prediction.prediction_mode == "learned_temporal_belief"
    fresh_scout_evidence_available = (
        belief.scout_freshness_seconds is not None and belief.scout_freshness_seconds <= 60.0
    )
    learned_tempo_threat_active = defensive_posture_gate_active or (
        fresh_scout_evidence_available
        and
        prediction.tech_risk >= config.tech_risk_threshold
        and prediction.confidence > config.low_information_confidence_threshold
        and belief.enemy_tech_signal_seen
    )
    bounded_production_tempo_gate_active = (
        config.production_tempo_gateway_delta > 0
        and learned_temporal_mode
        and belief.own_army_ready
        and learned_tempo_threat_active
    )

    selected_response_tag = "none"
    strategy_switch_reason = "none"
    if defensive_posture_gate_active:
        selected_response_tag = "defensive_posture"
        strategy_switch_reason = "adaptive_defensive_bias"
    elif bounded_production_tempo_gate_active:
        selected_response_tag = "bounded_production_tempo"
        strategy_switch_reason = "adaptive_production_tempo"
    elif continue_scouting_gate_active:
        selected_response_tag = "continue_scouting"
        strategy_switch_reason = "adaptive_information_gap"
    elif first_attack_timing_gate_active:
        selected_response_tag = "first_attack_timing_delay"
        strategy_switch_reason = belief.first_attack_timing_bias

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
        continue_scouting_gate_active=continue_scouting_gate_active,
        defensive_posture_gate_active=defensive_posture_gate_active,
        first_attack_timing_gate_active=first_attack_timing_gate_active,
        bounded_production_tempo_gate_active=bounded_production_tempo_gate_active,
        first_attack_delay_seconds=(
            config.first_attack_delay_seconds if first_attack_timing_gate_active else 0.0
        ),
        first_attack_army_buffer=(
            config.first_attack_army_buffer if first_attack_timing_gate_active else 0
        ),
        production_tempo_gateway_delta=(
            config.production_tempo_gateway_delta if bounded_production_tempo_gate_active else 0
        ),
        belief_summary=belief.to_dict(),
    )


def _macro_world_model_response_from_prediction(
    prediction: OpponentPrediction,
    config: OpponentModelConfig,
    belief: BeliefState,
) -> StrategyResponse:
    action = prediction.recommended_macro_action or "none"
    continue_scouting_gate_active = (
        belief.scout_continuation_recommended
        or prediction.confidence <= config.low_information_confidence_threshold
    )
    defensive_posture_gate_active = action == "defensive_hold"
    first_attack_timing_gate_active = action in {
        "defensive_hold",
        "delay_move_out",
        "move_out_window_open",
    }
    bounded_production_tempo_gate_active = action in {
        "add_production",
        "increase_production_tempo",
    }
    first_attack_delay_seconds = 0.0
    first_attack_army_buffer = 0
    if action in {"defensive_hold", "delay_move_out"}:
        first_attack_delay_seconds = config.first_attack_delay_seconds
        first_attack_army_buffer = config.first_attack_army_buffer
    elif action == "move_out_window_open":
        first_attack_delay_seconds = -float(config.first_attack_advance_seconds)
        first_attack_army_buffer = -max(1, int(config.first_attack_army_buffer))

    production_tempo_gateway_delta = 0
    if action == "add_production":
        production_tempo_gateway_delta = max(1, int(config.production_tempo_gateway_delta))
    elif action == "increase_production_tempo":
        production_tempo_gateway_delta = max(2, int(config.production_tempo_gateway_delta) + 1)

    selected_response_tag = action
    strategy_switch_reason = f"macro_action_selected:{action}"
    if action == "none" and continue_scouting_gate_active:
        selected_response_tag = "scout_or_rescout"
        strategy_switch_reason = "macro_information_gap_rescout"

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
        continue_scouting_gate_active=continue_scouting_gate_active,
        defensive_posture_gate_active=defensive_posture_gate_active,
        first_attack_timing_gate_active=first_attack_timing_gate_active,
        bounded_production_tempo_gate_active=bounded_production_tempo_gate_active,
        first_attack_delay_seconds=first_attack_delay_seconds,
        first_attack_army_buffer=first_attack_army_buffer,
        production_tempo_gateway_delta=production_tempo_gateway_delta,
        selected_macro_action=action,
        macro_action_scores=prediction.macro_action_scores,
        belief_summary=belief.to_dict(),
    )
