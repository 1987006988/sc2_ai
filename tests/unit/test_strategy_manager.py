from sc2bot.config.schema import OpponentModelConfig
from sc2bot.domain.decisions import StrategyResponse
from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.managers.strategy_manager import StrategyManager, build_belief_state
from sc2bot.opponent_model.interface import OpponentPrediction


def test_strategy_response_default_is_safe_noop():
    response = StrategyResponse()

    assert response.selected_response_tag == "none"
    assert response.strategy_switch_reason == "none"
    assert response.intervention_mode == "none"
    assert response.rush_risk == 0.0
    assert response.tech_risk == 0.0
    assert response.confidence == 0.0
    assert response.prediction_signals == ()
    assert response.recommended_response_tags == ()
    assert response.continue_scouting_gate_active is False
    assert response.defensive_posture_gate_active is False
    assert response.first_attack_timing_gate_active is False
    assert response.belief_summary == {}


def test_strategy_response_serializes_for_telemetry():
    response = StrategyResponse(
        selected_response_tag="defensive_posture",
        strategy_switch_reason="rush_risk_high",
        intervention_mode="tag_only",
        opponent_model_mode="rule_based",
        prediction_model_name="rule_based",
        prediction_mode="prediction_only",
        prediction_opening_type="combat_units_seen",
        rush_risk=0.8,
        tech_risk=0.2,
        confidence=0.7,
        prediction_signals=("early_combat_unit",),
        recommended_response_tags=("watch_for_rush",),
    )

    assert response.to_dict() == {
        "selected_response_tag": "defensive_posture",
        "strategy_switch_reason": "rush_risk_high",
        "intervention_mode": "tag_only",
        "opponent_model_mode": "rule_based",
        "prediction_model_name": "rule_based",
        "prediction_mode": "prediction_only",
        "prediction_opening_type": "combat_units_seen",
        "rush_risk": 0.8,
        "tech_risk": 0.2,
        "confidence": 0.7,
        "prediction_signals": ["early_combat_unit"],
        "recommended_response_tags": ["watch_for_rush"],
        "continue_scouting_gate_active": False,
        "defensive_posture_gate_active": False,
        "first_attack_timing_gate_active": False,
        "first_attack_delay_seconds": 0.0,
        "first_attack_army_buffer": 0,
        "belief_summary": {},
    }


def test_strategy_manager_tag_only_selects_continue_scouting_for_low_information():
    manager = StrategyManager()
    prediction = OpponentPrediction(model_name="rule_based", confidence=0.1)
    config = OpponentModelConfig(mode="rule_based", intervention_mode="tag_only")

    response = manager.select_response(
        GameState(game_loop=0, game_time=120.0),
        ScoutingObservation.empty(0),
        prediction,
        config,
    )

    assert response.selected_response_tag == "continue_scouting"
    assert response.strategy_switch_reason == "low_information"
    assert response.intervention_mode == "tag_only"
    assert response.opponent_model_mode == "rule_based"


def test_strategy_manager_tag_only_selects_defensive_posture_for_rush_risk():
    manager = StrategyManager()
    prediction = OpponentPrediction(
        model_name="rule_based",
        rush_risk=0.8,
        tech_risk=0.8,
        confidence=0.9,
        signals=("early_combat_unit",),
        recommended_response_tags=("watch_for_rush",),
    )
    config = OpponentModelConfig(mode="rule_based", intervention_mode="tag_only")

    response = manager.select_response(
        GameState(game_loop=0, game_time=30.0, visible_enemy_units_count=1),
        ScoutingObservation(
            game_loop=100,
            game_time=30.0,
            enemy_units_seen=("zergling",),
            seen_enemy_combat_units=("zergling",),
            observation_confidence=0.8,
        ),
        prediction,
        config,
    )

    assert response.selected_response_tag == "defensive_posture"
    assert response.strategy_switch_reason == "rush_risk_high"
    assert response.rush_risk == 0.8
    assert response.tech_risk == 0.8
    assert response.prediction_signals == ("early_combat_unit",)
    assert response.recommended_response_tags == ("watch_for_rush",)


def test_strategy_manager_minimal_behavior_selects_defensive_posture_for_rush_risk():
    manager = StrategyManager()
    prediction = OpponentPrediction(model_name="rule_based", rush_risk=0.8, confidence=0.9)
    config = OpponentModelConfig(mode="rule_based", intervention_mode="minimal_behavior")

    response = manager.select_response(
        GameState(game_loop=0, game_time=30.0, visible_enemy_units_count=1),
        ScoutingObservation(
            game_loop=100,
            game_time=30.0,
            enemy_units_seen=("zergling",),
            seen_enemy_combat_units=("zergling",),
            observation_confidence=0.8,
        ),
        prediction,
        config,
    )

    assert response.selected_response_tag == "defensive_posture"
    assert response.strategy_switch_reason == "rush_risk_high"
    assert response.intervention_mode == "minimal_behavior"


def test_strategy_manager_tag_only_selects_tech_alert_for_tech_risk():
    manager = StrategyManager()
    prediction = OpponentPrediction(
        model_name="rule_based",
        rush_risk=0.2,
        tech_risk=0.7,
        confidence=0.9,
        signals=("tech_or_gas",),
    )
    config = OpponentModelConfig(mode="rule_based", intervention_mode="tag_only")

    response = manager.select_response(
        GameState(game_loop=0, game_time=30.0),
        ScoutingObservation(
            game_loop=100,
            game_time=30.0,
            enemy_structures_seen=("cyberneticscore",),
            seen_enemy_structures=("cyberneticscore",),
            observation_confidence=0.9,
        ),
        prediction,
        config,
    )

    assert response.selected_response_tag == "tech_alert"
    assert response.strategy_switch_reason == "tech_risk_high"
    assert response.tech_risk == 0.7


def test_strategy_manager_non_tag_only_keeps_noop_response():
    manager = StrategyManager()
    prediction = OpponentPrediction(model_name="rule_based", rush_risk=0.8, confidence=0.9)
    config = OpponentModelConfig(mode="rule_based", intervention_mode="none")

    response = manager.select_response(
        GameState(game_loop=0, game_time=30.0),
        ScoutingObservation.empty(0),
        prediction,
        config,
    )

    assert response.selected_response_tag == "none"
    assert response.strategy_switch_reason == "none"
    assert response.intervention_mode == "none"


def test_build_belief_state_marks_information_gap_and_scout_continuation():
    belief = build_belief_state(
        state=GameState(game_loop=500, game_time=120.0, own_army_count=2),
        observation=ScoutingObservation.empty(500),
        prediction=OpponentPrediction(model_name="rule_based", confidence=0.1),
        config=OpponentModelConfig(mode="rule_based", intervention_mode="adaptive_gating"),
    )

    assert belief.enemy_contact_known is False
    assert belief.information_gap_high is True
    assert belief.scout_continuation_recommended is True
    assert belief.first_attack_timing_bias == "information_gap_delay"


def test_strategy_manager_adaptive_gating_sets_multiple_real_gate_flags():
    manager = StrategyManager()
    prediction = OpponentPrediction(
        model_name="rule_based",
        rush_risk=0.8,
        confidence=0.1,
        signals=("early_combat_unit", "low_information"),
    )
    config = OpponentModelConfig(
        mode="rule_based",
        intervention_mode="adaptive_gating",
        first_attack_delay_seconds=75.0,
        first_attack_army_buffer=3,
    )

    response = manager.select_response(
        GameState(
            game_loop=2000,
            game_time=120.0,
            own_army_count=3,
            known_enemy_start_location=(100.0, 100.0),
        ),
        ScoutingObservation.empty(2000),
        prediction,
        config,
    )

    assert response.intervention_mode == "adaptive_gating"
    assert response.selected_response_tag == "defensive_posture"
    assert response.defensive_posture_gate_active is True
    assert response.continue_scouting_gate_active is True
    assert response.first_attack_timing_gate_active is True
    assert response.first_attack_delay_seconds == 75.0
    assert response.first_attack_army_buffer == 3
    assert response.belief_summary["defensive_bias_active"] is True
