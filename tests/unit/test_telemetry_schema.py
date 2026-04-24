import json

from sc2bot.config.schema import (
    BotConfig,
    BotIdentityConfig,
    BuildOrderConfig,
    ManagersConfig,
    OpponentModelConfig,
    RuntimeConfig,
    TelemetryConfig,
)
from sc2bot.domain.game_state import GameState
from sc2bot.runtime.dependency_container import DependencyContainer
from sc2bot.runtime.game_loop import GameLoop
from sc2bot.telemetry.schema import SCHEMA_VERSION, TelemetryEvent


def test_telemetry_event_to_dict():
    event = TelemetryEvent(event_type="match_started", payload={"bot": "test"})
    data = event.to_dict()

    assert data["schema_version"] == SCHEMA_VERSION
    assert data["event_type"] == "match_started"
    assert data["payload"]["bot"] == "test"


def test_game_loop_records_prediction_only_opponent_prediction(tmp_path):
    config = BotConfig(
        bot=BotIdentityConfig(
            name="test-bot",
            race="protoss",
            strategy="test",
        ),
        managers=ManagersConfig(),
        opponent_model=OpponentModelConfig(mode="rule_based", intervention_mode="tag_only"),
        runtime=RuntimeConfig(),
        build_order=BuildOrderConfig(),
        telemetry=TelemetryConfig(output_dir=str(tmp_path)),
    )
    container = DependencyContainer.from_config(config)

    GameLoop(container).process_state(
        GameState(
            game_loop=100,
            game_time=4.5,
            visible_enemy_units_count=1,
            visible_enemy_units=("zergling",),
        )
    )

    events = [
        json.loads(line)
        for line in (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    prediction_event = next(
        event for event in events if event["event_type"] == "opponent_prediction"
    )
    strategy_event = next(
        event for event in events if event["event_type"] == "strategy_decision"
    )
    response_event = next(
        event for event in events if event["event_type"] == "strategy_response"
    )
    switch_event = next(event for event in events if event["event_type"] == "strategy_switch")
    combat_event = next(
        event for event in events if event["event_type"] == "combat_event_skipped"
    )

    assert prediction_event["payload"]["opponent_model_mode"] == "rule_based"
    assert prediction_event["payload"]["prediction"]["prediction_mode"] == "prediction_only"
    assert "early_combat_unit" in prediction_event["payload"]["prediction"]["signals"]
    assert strategy_event["payload"]["prediction_mode"] == "prediction_only"
    assert "early_combat_unit" in strategy_event["payload"]["prediction_signals"]
    assert response_event["payload"]["selected_response_tag"] == "defensive_posture"
    assert response_event["payload"]["strategy_switch_reason"] == "rush_risk_high"
    assert response_event["payload"]["intervention_mode"] == "tag_only"
    assert response_event["payload"]["opponent_model_mode"] == "rule_based"
    assert response_event["payload"]["prediction_mode"] == "prediction_only"
    assert response_event["payload"]["rush_risk"] == 0.55
    assert "early_combat_unit" in response_event["payload"]["prediction_signals"]
    assert switch_event["payload"]["selected_response_tag"] == "defensive_posture"
    assert switch_event["payload"]["strategy_switch_reason"] == "rush_risk_high"
    assert combat_event["payload"]["reason"] == "no_own_army_available"
    assert combat_event["payload"]["enemy_combat_unit_nearby"] is True
    assert combat_event["payload"]["planning_signal_present"] is False
    assert combat_event["payload"]["execution_evidence_available"] is False
