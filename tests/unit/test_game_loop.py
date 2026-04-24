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
from sc2bot.runtime.game_loop import (
    ARMY_PRESENCE_CONFIRMATION_GAME_LOOPS,
    DEFAULT_SUSTAIN_UNTIL_GAME_LOOP,
    GameLoop,
    active_alert_names_from_bot_ai,
    assimilator_build_skip_reason,
    build_army_presence_payload,
    build_combat_unit_lifecycle_payload,
    build_combat_unit_production_payload,
    build_combat_unit_queue_payload,
    build_gateway_build_payload,
    build_minimal_behavior_intervention_payload,
    build_supply_sustain_payload,
    build_tech_structure_payload,
    classify_army_presence_events,
    combat_unit_production_skip_reason,
    cybernetics_core_build_skip_reason,
    documented_army_count_from_bot_ai,
    gateway_build_skip_reason,
    legacy_own_army_count_from_bot_ai,
    normalize_available_ability_names,
    record_minimal_behavior_intervention,
    select_combat_unit_for_production,
    should_leave_after_sustain_limit,
    units_created_count_from_bot_ai,
)
from sc2bot.domain.decisions import StrategyResponse
from sc2bot.telemetry.event_logger import EventLogger


def test_should_leave_after_sustain_limit_waits_before_limit():
    assert not should_leave_after_sustain_limit(DEFAULT_SUSTAIN_UNTIL_GAME_LOOP - 1)


def test_should_leave_after_sustain_limit_leaves_at_limit():
    assert should_leave_after_sustain_limit(DEFAULT_SUSTAIN_UNTIL_GAME_LOOP)


def test_build_supply_sustain_payload_has_stable_shape():
    payload = build_supply_sustain_payload(
        reason="insufficient_minerals",
        supply_used=14,
        supply_cap=15,
        runtime=RuntimeConfig(supply_sustain_threshold=2, supply_structure_name="pylon"),
    )

    assert payload == {
        "reason": "insufficient_minerals",
        "supply_used": 14,
        "supply_cap": 15,
        "threshold": 2,
        "structure": "pylon",
    }


def test_game_loop_records_strategy_switch_only_when_response_changes(tmp_path):
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
    loop = GameLoop(container)
    state = GameState(
        game_loop=100,
        game_time=4.5,
        visible_enemy_units_count=1,
        visible_enemy_units=("zergling",),
    )

    loop.process_state(state)
    loop.process_state(state)

    events = [
        json.loads(line)
        for line in (tmp_path / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert sum(1 for event in events if event["event_type"] == "strategy_response") == 2
    assert sum(1 for event in events if event["event_type"] == "strategy_switch") == 1


def test_build_minimal_behavior_intervention_payload_has_stable_shape():
    response = StrategyResponse(
        selected_response_tag="defensive_posture",
        strategy_switch_reason="rush_risk_high",
        intervention_mode="minimal_behavior",
    )

    payload = build_minimal_behavior_intervention_payload(
        response,
        action="army_defense",
        outcome="active",
        reason="defensive_posture",
    )

    assert payload == {
        "action": "army_defense",
        "outcome": "active",
        "reason": "defensive_posture",
        "selected_response_tag": "defensive_posture",
        "strategy_switch_reason": "rush_risk_high",
        "intervention_mode": "minimal_behavior",
    }


def test_record_minimal_behavior_intervention_writes_dry_telemetry(tmp_path):
    response = StrategyResponse(
        selected_response_tag="continue_scouting",
        strategy_switch_reason="low_information",
        intervention_mode="minimal_behavior",
    )
    telemetry = EventLogger(tmp_path)

    record_minimal_behavior_intervention(
        telemetry,
        response,
        action="scout_persistence",
        outcome="active",
        reason="continue_scouting",
    )

    event = json.loads((tmp_path / "events.jsonl").read_text(encoding="utf-8"))

    assert event["event_type"] == "minimal_behavior_intervention"
    assert event["payload"]["action"] == "scout_persistence"
    assert event["payload"]["outcome"] == "active"
    assert event["payload"]["selected_response_tag"] == "continue_scouting"


def test_gateway_build_skip_reason_waits_for_configured_conditions():
    build_order = BuildOrderConfig(gateway_min_probe_count=16, gateway_min_game_time=90.0)

    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=0, minerals=200, game_time=100.0),
            build_order,
        )
        == "no_worker_available"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=100, game_time=100.0),
            build_order,
        )
        == "insufficient_minerals"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=12, minerals=200, game_time=100.0),
            build_order,
        )
        == "insufficient_probe_count"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=200, game_time=60.0),
            build_order,
        )
        == "gateway_timing_not_reached"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=200, game_time=100.0),
            build_order,
            pending_gateway_count=1,
        )
        == "gateway_already_pending"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=200, game_time=100.0),
            build_order,
            existing_gateway_count=1,
        )
        == "gateway_already_exists"
    )
    assert (
        gateway_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=200, game_time=100.0),
            build_order,
        )
        is None
    )


def test_build_gateway_build_payload_has_stable_shape():
    state = GameState(
        game_loop=512,
        game_time=22.8,
        own_workers_count=16,
        minerals=175,
    )
    build_order = BuildOrderConfig(gateway_min_probe_count=16, gateway_min_game_time=90.0)

    payload = build_gateway_build_payload(
        "gateway_conditions_met",
        state,
        build_order,
        pending_gateway_count=0,
        existing_gateway_count=0,
    )

    assert payload == {
        "reason": "gateway_conditions_met",
        "structure": "gateway",
        "game_loop": 512,
        "game_time": 22.8,
        "minerals": 175,
        "own_workers_count": 16,
        "gateway_min_probe_count": 16,
        "gateway_min_game_time": 90.0,
        "pending_gateway_count": 0,
        "existing_gateway_count": 0,
    }


def test_gateway_build_payload_records_as_dry_telemetry(tmp_path):
    telemetry = EventLogger(tmp_path)
    payload = build_gateway_build_payload(
        "insufficient_minerals",
        GameState(game_loop=32, game_time=1.4, own_workers_count=12, minerals=75),
        BuildOrderConfig(),
    )

    telemetry.record("gateway_build_skipped", payload)

    event = json.loads((tmp_path / "events.jsonl").read_text(encoding="utf-8"))

    assert event["event_type"] == "gateway_build_skipped"
    assert event["payload"]["reason"] == "insufficient_minerals"
    assert event["payload"]["structure"] == "gateway"


def test_assimilator_build_skip_reason_waits_for_gateway_and_config():
    state = GameState(game_loop=0, own_workers_count=16, minerals=100, game_time=100.0)

    assert (
        assimilator_build_skip_reason(
            state,
            BuildOrderConfig(assimilator_enabled=False),
            gateway_ready_count=1,
        )
        == "assimilator_disabled"
    )
    assert (
        assimilator_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=0,
        )
        == "gateway_not_ready"
    )
    assert (
        assimilator_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
            pending_assimilator_count=1,
        )
        == "assimilator_already_pending"
    )
    assert (
        assimilator_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
            existing_assimilator_count=1,
        )
        == "assimilator_already_exists"
    )
    assert (
        assimilator_build_skip_reason(
            GameState(game_loop=0, own_workers_count=0, minerals=100, game_time=100.0),
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        == "no_worker_available"
    )
    assert (
        assimilator_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=50, game_time=100.0),
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        == "insufficient_minerals"
    )
    assert (
        assimilator_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        is None
    )


def test_cybernetics_core_build_skip_reason_waits_for_gateway_and_config():
    state = GameState(game_loop=0, own_workers_count=16, minerals=200, game_time=100.0)

    assert (
        cybernetics_core_build_skip_reason(
            state,
            BuildOrderConfig(cybernetics_core_enabled=False),
            gateway_ready_count=1,
        )
        == "cybernetics_core_disabled"
    )
    assert (
        cybernetics_core_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=0,
        )
        == "gateway_not_ready"
    )
    assert (
        cybernetics_core_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
            pending_cybernetics_core_count=1,
        )
        == "cybernetics_core_already_pending"
    )
    assert (
        cybernetics_core_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
            existing_cybernetics_core_count=1,
        )
        == "cybernetics_core_already_exists"
    )
    assert (
        cybernetics_core_build_skip_reason(
            GameState(game_loop=0, own_workers_count=0, minerals=200, game_time=100.0),
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        == "no_worker_available"
    )
    assert (
        cybernetics_core_build_skip_reason(
            GameState(game_loop=0, own_workers_count=16, minerals=100, game_time=100.0),
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        == "insufficient_minerals"
    )
    assert (
        cybernetics_core_build_skip_reason(
            state,
            BuildOrderConfig(),
            gateway_ready_count=1,
        )
        is None
    )


def test_build_tech_structure_payload_has_stable_shape():
    payload = build_tech_structure_payload(
        "gateway_not_ready",
        "cybernetics_core",
        GameState(
            game_loop=2048,
            game_time=91.4,
            minerals=125,
            vespene=10,
            own_workers_count=18,
        ),
        gateway_ready_count=0,
        pending_count=0,
        existing_count=0,
    )

    assert payload == {
        "reason": "gateway_not_ready",
        "structure": "cybernetics_core",
        "game_loop": 2048,
        "game_time": 91.4,
        "minerals": 125,
        "vespene": 10,
        "own_workers_count": 18,
        "gateway_ready_count": 0,
        "pending_count": 0,
        "existing_count": 0,
    }


def test_tech_structure_payload_records_as_dry_telemetry(tmp_path):
    telemetry = EventLogger(tmp_path)
    payload = build_tech_structure_payload(
        "insufficient_minerals",
        "assimilator",
        GameState(game_loop=32, game_time=1.4, own_workers_count=12, minerals=50),
        gateway_ready_count=1,
        pending_count=0,
        existing_count=0,
    )

    telemetry.record("assimilator_build_skipped", payload)

    event = json.loads((tmp_path / "events.jsonl").read_text(encoding="utf-8"))

    assert event["event_type"] == "assimilator_build_skipped"
    assert event["payload"]["reason"] == "insufficient_minerals"
    assert event["payload"]["structure"] == "assimilator"


def test_combat_unit_production_skip_reason_is_structured():
    state = GameState(game_loop=0, game_time=0.0, minerals=200, vespene=100)

    assert (
        combat_unit_production_skip_reason(
            state,
            "zealot",
            gateway_ready_count=0,
        )
        == "gateway_not_ready"
    )
    assert (
        combat_unit_production_skip_reason(
            GameState(game_loop=0, game_time=0.0, minerals=50, vespene=100),
            "zealot",
            gateway_ready_count=1,
        )
        == "insufficient_minerals"
    )
    assert (
        combat_unit_production_skip_reason(
            state,
            "stalker",
            gateway_ready_count=1,
            cybernetics_core_ready_count=0,
        )
        == "cybernetics_core_not_ready"
    )
    assert (
        combat_unit_production_skip_reason(
            GameState(game_loop=0, game_time=0.0, minerals=100, vespene=100),
            "stalker",
            gateway_ready_count=1,
            cybernetics_core_ready_count=1,
        )
        == "insufficient_minerals"
    )
    assert (
        combat_unit_production_skip_reason(
            GameState(game_loop=0, game_time=0.0, minerals=200, vespene=0),
            "stalker",
            gateway_ready_count=1,
            cybernetics_core_ready_count=1,
        )
        == "insufficient_vespene"
    )
    assert (
        combat_unit_production_skip_reason(
            state,
            "stalker",
            gateway_ready_count=1,
            cybernetics_core_ready_count=1,
        )
        is None
    )
    assert (
        combat_unit_production_skip_reason(
            state,
            "carrier",
            gateway_ready_count=1,
            cybernetics_core_ready_count=1,
        )
        == "unsupported_combat_unit"
    )


def test_select_combat_unit_for_production_uses_priority_and_prerequisites():
    zealot_first = BuildOrderConfig(
        zealot_production_priority=10,
        stalker_production_priority=20,
    )
    stalker_first = BuildOrderConfig(
        zealot_production_priority=20,
        stalker_production_priority=10,
    )
    state = GameState(game_loop=0, game_time=0.0, minerals=200, vespene=100)

    assert select_combat_unit_for_production(
        state,
        zealot_first,
        gateway_ready_count=1,
        cybernetics_core_ready_count=1,
    ) == ("zealot", None)
    assert select_combat_unit_for_production(
        state,
        stalker_first,
        gateway_ready_count=1,
        cybernetics_core_ready_count=1,
    ) == ("stalker", None)
    assert select_combat_unit_for_production(
        state,
        stalker_first,
        gateway_ready_count=1,
        cybernetics_core_ready_count=0,
    ) == ("zealot", None)
    assert select_combat_unit_for_production(
        GameState(game_loop=0, game_time=0.0, minerals=50, vespene=0),
        zealot_first,
        gateway_ready_count=1,
        cybernetics_core_ready_count=0,
    ) == (None, "insufficient_minerals")


def test_build_combat_unit_production_payload_has_stable_shape():
    payload = build_combat_unit_production_payload(
        "combat_unit_conditions_met",
        "zealot",
        GameState(
            game_loop=3000,
            game_time=133.9,
            minerals=140,
            vespene=25,
            supply_used=24,
            supply_cap=31,
        ),
        gateway_ready_count=1,
        cybernetics_core_ready_count=0,
        idle_gateway_count=1,
    )

    assert payload == {
        "reason": "combat_unit_conditions_met",
        "unit": "zealot",
        "evidence_semantics": "precondition_or_command_path_only",
        "game_loop": 3000,
        "game_time": 133.9,
        "minerals": 140,
        "vespene": 25,
        "supply_used": 24,
        "supply_cap": 31,
        "gateway_ready_count": 1,
        "cybernetics_core_ready_count": 0,
        "idle_gateway_count": 1,
        "pending_before_train": 0,
        "pending_after_train": 0,
        "pending_after_train_delta": 0,
        "available_gateway_abilities": [],
        "active_alerts": [],
        "units_created_total_for_unit": 0,
    }


def test_combat_unit_production_payload_records_as_dry_telemetry(tmp_path):
    telemetry = EventLogger(tmp_path)
    payload = build_combat_unit_production_payload(
        "gateway_not_ready",
        None,
        GameState(game_loop=0, game_time=0.0, minerals=50, vespene=0),
        gateway_ready_count=0,
        cybernetics_core_ready_count=0,
        idle_gateway_count=0,
    )

    telemetry.record("combat_unit_production_skipped", payload)

    event = json.loads((tmp_path / "events.jsonl").read_text(encoding="utf-8"))

    assert event["event_type"] == "combat_unit_production_skipped"
    assert event["payload"]["reason"] == "gateway_not_ready"
    assert event["payload"]["unit"] == "none"
    assert event["payload"]["evidence_semantics"] == "precondition_or_command_path_only"


def test_build_army_presence_payload_has_stable_shape():
    payload = build_army_presence_payload(
        "first_combat_unit_created",
        GameState(
            game_loop=6400,
            game_time=285.7,
            own_army_count=1,
            visible_enemy_units_count=0,
            visible_enemy_structures_count=3,
        ),
        previous_army_count=0,
    )

    assert payload == {
        "reason": "first_combat_unit_created",
        "game_loop": 6400,
        "game_time": 285.7,
        "previous_army_count": 0,
        "own_army_count": 1,
        "observed_unit_tag": None,
        "observed_unit_type": None,
        "observation_source": "bot_ai.army",
        "legacy_own_army_count": None,
        "documented_own_army_count": None,
        "combat_unit_count": None,
        "visible_enemy_units_count": 0,
        "visible_enemy_structures_count": 3,
    }


def test_build_combat_unit_lifecycle_payload_has_stable_shape():
    payload = build_combat_unit_lifecycle_payload(
        "alive_after_short_window",
        GameState(game_loop=6467, game_time=288.7, own_army_count=1),
        unit_tag=77,
        unit_name="zealot",
        first_observed_game_loop=6400,
    )

    assert payload == {
        "reason": "alive_after_short_window",
        "unit_tag": 77,
        "unit": "zealot",
        "game_loop": 6467,
        "game_time": 288.7,
        "own_army_count": 1,
        "first_observed_game_loop": 6400,
        "confirmation_window_game_loops": ARMY_PRESENCE_CONFIRMATION_GAME_LOOPS,
        "confirmation_window_seconds": round(ARMY_PRESENCE_CONFIRMATION_GAME_LOOPS / 22.4, 2),
        "observation_source": "bot_ai.army",
        "legacy_own_army_count": None,
        "documented_own_army_count": None,
        "combat_unit_count": None,
        "units_created_total_for_unit": None,
    }


def test_build_combat_unit_queue_payload_has_stable_shape():
    payload = build_combat_unit_queue_payload(
        "queue_entry_observed_after_train",
        "zealot",
        GameState(game_loop=3128, game_time=139.64),
        pending_before_train=0,
        pending_after_train=1,
        available_gateway_abilities=("TRAIN_ZEALOT",),
        active_alerts=("TrainUnitComplete",),
    )

    assert payload == {
        "reason": "queue_entry_observed_after_train",
        "unit": "zealot",
        "game_loop": 3128,
        "game_time": 139.64,
        "pending_before_train": 0,
        "pending_after_train": 1,
        "pending_after_train_delta": 1,
        "available_gateway_abilities": ["TRAIN_ZEALOT"],
        "active_alerts": ["TrainUnitComplete"],
        "evidence_semantics": "queued_not_created",
    }


def test_classify_army_presence_events_distinguishes_observed_presence_from_short_window_alive():
    initial_state = GameState(game_loop=6400, game_time=285.7, own_army_count=1)
    initial_events, first_seen, confirmed, current_tags = classify_army_presence_events(
        initial_state,
        ((77, "zealot"),),
        previous_army_count=0,
        previous_observed_tags=set(),
        first_observed_game_loops={},
        confirmed_army_tags=set(),
    )

    assert [event_type for event_type, _payload in initial_events] == ["army_presence_changed"]
    assert initial_events[0][1]["reason"] == "first_observed_army_presence"
    assert initial_events[0][1]["observed_unit_type"] == "zealot"
    assert first_seen == {77: 6400}
    assert confirmed == set()
    assert current_tags == {77}

    confirmed_state = GameState(
        game_loop=6400 + ARMY_PRESENCE_CONFIRMATION_GAME_LOOPS,
        game_time=288.7,
        own_army_count=1,
    )
    confirmed_events, next_first_seen, next_confirmed, next_tags = classify_army_presence_events(
        confirmed_state,
        ((77, "zealot"),),
        previous_army_count=1,
        previous_observed_tags=current_tags,
        first_observed_game_loops=first_seen,
        confirmed_army_tags=confirmed,
    )

    assert [event_type for event_type, _payload in confirmed_events] == [
        "unit_alive_after_short_window",
    ]
    assert confirmed_events[0][1]["reason"] == "alive_after_short_window"
    assert next_first_seen == {77: 6400}
    assert next_confirmed == {77}
    assert next_tags == {77}


def test_documented_army_count_prefers_documented_channel():
    class FakeBot:
        army_count = 3
        army = [object(), object()]

    bot = FakeBot()

    assert legacy_own_army_count_from_bot_ai(bot) == 2
    assert documented_army_count_from_bot_ai(bot, fallback_count=2) == 3


def test_units_created_count_reads_specific_unit_name():
    class FakeType:
        def __init__(self, name):
            self.name = name

    class FakeBot:
        units_created = {
            FakeType("ZEALOT"): 2,
            FakeType("STALKER"): 1,
        }

    bot = FakeBot()

    assert units_created_count_from_bot_ai(bot, "zealot") == 2
    assert units_created_count_from_bot_ai(bot, "stalker") == 1
    assert units_created_count_from_bot_ai(bot, "probe") == 0


def test_normalize_available_ability_names_deduplicates_names():
    class FakeAbility:
        def __init__(self, name):
            self.name = name

    abilities = (FakeAbility("TRAIN_ZEALOT"), FakeAbility("TRAIN_ZEALOT"))

    assert normalize_available_ability_names(abilities) == ("TRAIN_ZEALOT",)


def test_active_alert_names_uses_alert_name_when_present():
    class FakeAlert:
        def __init__(self, name):
            self.name = name

    class FakeState:
        alerts = (FakeAlert("TrainError"), FakeAlert("TrainUnitComplete"))

    class FakeBot:
        state = FakeState()

    assert active_alert_names_from_bot_ai(FakeBot()) == (
        "TrainError",
        "TrainUnitComplete",
    )
