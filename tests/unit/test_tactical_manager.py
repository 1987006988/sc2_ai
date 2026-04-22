from sc2bot.config.schema import BuildOrderConfig
from sc2bot.domain.decisions import StrategyDecision, TacticalPlan
from sc2bot.domain.game_state import GameState
from sc2bot.managers.tactical_manager import TacticalManager, build_combat_event_payload


def test_tactical_plan_serializes_army_order_fields():
    plan = TacticalPlan(
        name="basic_attack_order",
        strategy="default",
        tags=("attack_order",),
        order="attack_order",
        reason="army_or_time_threshold_met",
        rally_point=(10.0, 20.0),
        target_position=(90.0, 80.0),
        own_army_count=8,
        visible_enemy_units_count=0,
    )

    assert plan.to_dict() == {
        "name": "basic_attack_order",
        "strategy": "default",
        "tags": ["attack_order"],
        "order": "attack_order",
        "reason": "army_or_time_threshold_met",
        "rally_point": [10.0, 20.0],
        "target_position": [90.0, 80.0],
        "own_army_count": 8,
        "visible_enemy_units_count": 0,
    }


def test_tactical_manager_rallies_before_attack_or_defend_conditions():
    plan = TacticalManager().plan(
        GameState(
            game_loop=0,
            game_time=60.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=1,
        ),
        StrategyDecision("default"),
    )

    assert plan.order == "army_rally"
    assert plan.reason == "waiting_for_attack_or_defend_condition"
    assert plan.target_position == (10.0, 20.0)


def test_tactical_manager_defends_when_enemy_units_visible():
    plan = TacticalManager().plan(
        GameState(
            game_loop=0,
            game_time=60.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=(90.0, 80.0),
            visible_enemy_units_count=2,
            own_army_count=3,
        ),
        StrategyDecision("default"),
    )

    assert plan.order == "defend_order"
    assert plan.reason == "enemy_units_visible_near_base"
    assert plan.target_position == (10.0, 20.0)


def test_tactical_manager_attacks_after_army_threshold():
    plan = TacticalManager(
        BuildOrderConfig(attack_army_supply_threshold=4, attack_game_time_threshold=999.0)
    ).plan(
        GameState(
            game_loop=0,
            game_time=120.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=4,
        ),
        StrategyDecision("default"),
    )

    assert plan.order == "attack_order"
    assert plan.reason == "army_or_time_threshold_met"
    assert plan.target_position == (90.0, 80.0)


def test_tactical_manager_attacks_after_time_threshold():
    plan = TacticalManager(
        BuildOrderConfig(attack_army_supply_threshold=99, attack_game_time_threshold=120.0)
    ).plan(
        GameState(
            game_loop=0,
            game_time=120.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=0,
        ),
        StrategyDecision("default"),
    )

    assert plan.order == "attack_order"
    assert plan.reason == "army_or_time_threshold_met"
    assert plan.target_position == (90.0, 80.0)


def test_build_combat_event_payload_detects_enemy_combat_unit_nearby():
    plan = TacticalPlan(
        name="basic_defend_order",
        strategy="default",
        order="defend_order",
        reason="enemy_units_visible_near_base",
        target_position=(10.0, 20.0),
        own_army_count=0,
        visible_enemy_units_count=2,
    )
    payload = build_combat_event_payload(
        GameState(
            game_loop=44,
            game_time=2.0,
            own_start_location=(10.0, 20.0),
            visible_enemy_units_count=2,
            own_army_count=0,
        ),
        plan,
    )

    assert payload["detected"] is True
    assert payload["reason"] == "combat_signal_detected"
    assert payload["enemy_combat_unit_nearby"] is True
    assert payload["own_army_near_enemy"] is False


def test_build_combat_event_payload_detects_attack_order_near_enemy():
    plan = TacticalPlan(
        name="basic_attack_order",
        strategy="default",
        order="attack_order",
        reason="army_or_time_threshold_met",
        target_position=(90.0, 80.0),
        own_army_count=4,
    )
    payload = build_combat_event_payload(
        GameState(
            game_loop=4000,
            game_time=180.0,
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=4,
        ),
        plan,
    )

    assert payload["detected"] is True
    assert payload["attack_order_near_enemy"] is True
    assert payload["target_position"] == [90.0, 80.0]


def test_build_combat_event_payload_has_structured_no_combat_reason():
    plan = TacticalPlan(
        name="basic_army_rally",
        strategy="default",
        order="army_rally",
        reason="waiting_for_attack_or_defend_condition",
        target_position=(10.0, 20.0),
        own_army_count=0,
    )
    payload = build_combat_event_payload(
        GameState(game_loop=0, game_time=0.0, own_army_count=0),
        plan,
    )

    assert payload["detected"] is False
    assert payload["reason"] == "no_own_army_available"
    assert payload["enemy_combat_unit_nearby"] is False
    assert payload["own_army_near_enemy"] is False
    assert payload["attack_order_near_enemy"] is False
