from pathlib import Path

from sc2bot.config.loader import load_bot_config
from sc2bot.config.schema import BuildOrderConfig, OpponentModelConfig
from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.managers.strategy_manager import StrategyManager
from sc2bot.opponent_model.interface import OpponentPrediction
from sc2bot.runtime.game_loop import _effective_build_order_from_strategy_response


def test_r7_world_model_config_loads_runtime_export_path():
    config = load_bot_config(Path("configs/bot/r7_world_model_advisor.yaml"))

    assert config.opponent_model.mode == "learned_world_model_advisor"
    assert config.opponent_model.intervention_mode == "macro_world_model_advisor"
    assert config.opponent_model.model_checkpoint_path.endswith(
        "scratch_ensemble_v0_runtime.json"
    )
    assert config.opponent_model.first_attack_advance_seconds == 30.0


def test_r7_rule_macro_config_loads_comparator_mode():
    config = load_bot_config(Path("configs/bot/r7_rule_macro_advisor.yaml"))

    assert config.opponent_model.mode == "rule_based_macro_advisor"
    assert config.opponent_model.intervention_mode == "macro_world_model_advisor"
    assert config.opponent_model.production_tempo_gateway_delta == 1


def test_macro_world_model_strategy_maps_add_production_to_gateway_delta():
    response = StrategyManager().select_response(
        state=GameState(game_loop=800, game_time=120.0, own_army_count=3),
        observation=ScoutingObservation.empty(800),
        prediction=OpponentPrediction(
            model_name="r7_world_model_runtime_v0",
            prediction_mode="learned_world_model_advisor",
            recommended_macro_action="add_production",
            macro_action_scores={"add_production": 0.8},
            confidence=0.6,
        ),
        config=OpponentModelConfig(
            mode="learned_world_model_advisor",
            intervention_mode="macro_world_model_advisor",
            production_tempo_gateway_delta=1,
        ),
    )

    assert response.selected_macro_action == "add_production"
    assert response.bounded_production_tempo_gate_active is True
    assert response.production_tempo_gateway_delta == 1


def test_macro_world_model_strategy_maps_move_out_to_signed_attack_release():
    response = StrategyManager().select_response(
        state=GameState(game_loop=2400, game_time=180.0, own_army_count=8),
        observation=ScoutingObservation.empty(2400),
        prediction=OpponentPrediction(
            model_name="r7_world_model_runtime_v0",
            prediction_mode="learned_world_model_advisor",
            recommended_macro_action="move_out_window_open",
            macro_action_scores={"move_out_window_open": 0.8},
            confidence=0.7,
        ),
        config=OpponentModelConfig(
            mode="learned_world_model_advisor",
            intervention_mode="macro_world_model_advisor",
            first_attack_advance_seconds=30.0,
            first_attack_army_buffer=1,
        ),
    )

    assert response.selected_macro_action == "move_out_window_open"
    assert response.first_attack_timing_gate_active is True
    assert response.first_attack_delay_seconds == -30.0
    assert response.first_attack_army_buffer == -1


def test_effective_build_order_prefers_stalkers_for_add_tech():
    effective = _effective_build_order_from_strategy_response(
        BuildOrderConfig(zealot_production_priority=10, stalker_production_priority=20),
        StrategyManager().select_response(
            state=GameState(game_loop=1400, game_time=90.0, own_army_count=2),
            observation=ScoutingObservation.empty(1400),
            prediction=OpponentPrediction(
                model_name="r7_world_model_runtime_v0",
                prediction_mode="learned_world_model_advisor",
                recommended_macro_action="add_tech",
                macro_action_scores={"add_tech": 0.7},
            ),
            config=OpponentModelConfig(
                mode="learned_world_model_advisor",
                intervention_mode="macro_world_model_advisor",
            ),
        ),
    )

    assert effective.stalker_production_priority < effective.zealot_production_priority
