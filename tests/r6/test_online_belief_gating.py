from pathlib import Path

import torch

from sc2bot.config.loader import load_bot_config
from sc2bot.config.schema import BuildOrderConfig, OpponentModelConfig
from sc2bot.domain.game_state import GameState
from sc2bot.opponent_model.interface import OpponentPrediction
from sc2bot.domain.decisions import StrategyResponse
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.managers.strategy_manager import StrategyManager
from sc2bot.opponent_model.temporal_belief_model import TemporalBeliefModel
from sc2bot.opponent_model.temporal_runtime_model import (
    TemporalBeliefOpponentModel,
    observation_to_temporal_frame,
)
from sc2bot.runtime.game_loop import _effective_build_order_from_strategy_response


def test_r6_learned_belief_config_loads_frontier_treatment_fields():
    config = load_bot_config(Path("configs/bot/r6_learned_belief.yaml"))

    assert config.opponent_model.mode == "learned_temporal_belief"
    assert config.opponent_model.model_checkpoint_path.endswith("temporal_gru_v0.pt")
    assert config.opponent_model.temporal_history_window == 8
    assert config.opponent_model.production_tempo_gateway_delta == 1


def test_temporal_runtime_observation_frame_is_schema_compatible():
    frame = observation_to_temporal_frame(
        ScoutingObservation(
            game_loop=100,
            game_time=45.0,
            current_enemy_structures=("SpawningPool", "Extractor"),
            current_enemy_combat_units=("zergling",),
            seen_enemy_structures=("SpawningPool", "Extractor"),
            seen_enemy_combat_units=("zergling",),
            enemy_expansion_seen=False,
            possible_tech_signal=False,
            possible_rush_signal=True,
        )
    )

    assert frame["enemy_gas_structures"] == 1
    assert frame["enemy_production_structures"] >= 1
    assert frame["enemy_contact_seen"] is True
    assert frame["enemy_tech_path_hint"] in {"gas_tech", "unknown"}


def test_temporal_runtime_model_emits_learned_prediction_mode(tmp_path: Path):
    model = TemporalBeliefModel(input_dim=12, hidden_dim=8)
    checkpoint_path = tmp_path / "temporal.pt"
    torch.save({"model_state_dict": model.state_dict(), "hidden_dim": 8}, checkpoint_path)
    runtime_model = TemporalBeliefOpponentModel(str(checkpoint_path), history_window=4)

    prediction = runtime_model.predict(
        ScoutingObservation(
            game_loop=1,
            game_time=15.0,
            seen_enemy_structures=("Gateway",),
            seen_enemy_combat_units=(),
            observation_confidence=0.4,
        )
    )

    assert prediction.prediction_mode == "learned_temporal_belief"
    assert prediction.model_name == "temporal_gru_v0"


def test_adaptive_strategy_can_activate_bounded_production_tempo_for_learned_mode():
    response = StrategyManager().select_response(
        state=GameState(
            game_loop=2200,
            game_time=120.0,
            own_army_count=3,
            known_enemy_start_location=(90.0, 90.0),
        ),
        observation=ScoutingObservation.empty(2200),
        prediction=OpponentPrediction(
            model_name="temporal_gru_v0",
            prediction_mode="learned_temporal_belief",
            rush_risk=0.8,
            tech_risk=0.6,
            confidence=0.2,
        ),
        config=OpponentModelConfig(
            mode="learned_temporal_belief",
            intervention_mode="adaptive_gating",
            rush_risk_threshold=0.65,
            tech_risk_threshold=0.5,
            production_tempo_gateway_delta=1,
        ),
    )

    assert response.bounded_production_tempo_gate_active is True
    assert response.production_tempo_gateway_delta == 1


def test_effective_build_order_applies_gateway_delta_only_when_gate_is_active():
    base = BuildOrderConfig(gateway_target_count=3)

    unchanged = _effective_build_order_from_strategy_response(base, StrategyResponse())
    changed = _effective_build_order_from_strategy_response(
        base,
        StrategyResponse(
            bounded_production_tempo_gate_active=True,
            production_tempo_gateway_delta=1,
        ),
    )

    assert unchanged.gateway_target_count == 3
    assert changed.gateway_target_count == 4
