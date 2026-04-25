from sc2bot.config.schema import BuildOrderConfig
from sc2bot.domain.decisions import StrategyDecision, StrategyResponse, TacticalPlan
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
        "defend_reason": None,
        "attack_reason": None,
        "regroup_reason": None,
        "rally_eligible": False,
        "order_prerequisites_met": False,
        "execution_evidence": "planning_only",
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
    assert plan.regroup_reason == "waiting_for_attack_or_defend_condition"
    assert plan.rally_eligible is True
    assert plan.order_prerequisites_met is True
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
    assert plan.defend_reason == "enemy_units_visible_near_base"
    assert plan.rally_eligible is False
    assert plan.order_prerequisites_met is True
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
    assert plan.reason == "army_threshold_met_with_known_enemy_start"
    assert plan.attack_reason == "army_threshold_met_with_known_enemy_start"
    assert plan.rally_eligible is False
    assert plan.order_prerequisites_met is True
    assert plan.target_position == (90.0, 80.0)


def test_tactical_manager_adaptive_attack_delay_holds_before_buffer_is_met():
    plan = TacticalManager(
        BuildOrderConfig(attack_army_supply_threshold=4, attack_game_time_threshold=120.0)
    ).plan(
        GameState(
            game_loop=0,
            game_time=120.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=4,
        ),
        StrategyDecision("default"),
        StrategyResponse(
            intervention_mode="adaptive_gating",
            first_attack_timing_gate_active=True,
            first_attack_delay_seconds=60.0,
            first_attack_army_buffer=2,
        ),
    )

    assert plan.order == "army_rally"
    assert plan.reason == "adaptive_attack_delay_active"
    assert plan.regroup_reason == "adaptive_attack_delay_active"
    assert plan.rally_eligible is True


def test_tactical_manager_does_not_attack_without_army_even_after_time_threshold():
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

    assert plan.order == "hold_position"
    assert plan.reason == "no_army_available"
    assert plan.regroup_reason == "no_army_available"
    assert plan.rally_eligible is False
    assert plan.order_prerequisites_met is False
    assert plan.target_position == (10.0, 20.0)


def test_build_combat_event_payload_does_not_claim_combat_from_enemy_visibility_only():
    plan = TacticalPlan(
        name="basic_defend_order",
        strategy="default",
        order="defend_order",
        reason="enemy_units_visible_near_base",
        defend_reason="enemy_units_visible_near_base",
        order_prerequisites_met=False,
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

    assert payload["detected"] is False
    assert payload["reason"] == "no_own_army_available"
    assert payload["planning_signal_present"] is True
    assert payload["execution_evidence_available"] is False
    assert payload["enemy_combat_unit_nearby"] is True
    assert payload["own_army_near_enemy"] is False
    assert payload["rally_eligible"] is False


def test_build_combat_event_payload_marks_attack_plan_as_planning_only_without_execution_evidence():
    plan = TacticalPlan(
        name="basic_attack_order",
        strategy="default",
        order="attack_order",
        reason="army_threshold_met_with_known_enemy_start",
        attack_reason="army_threshold_met_with_known_enemy_start",
        order_prerequisites_met=True,
        target_position=(90.0, 80.0),
        own_army_count=4,
    )
    payload = build_combat_event_payload(
        GameState(
            game_loop=4000,
            game_time=180.0,
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=4,
            visible_enemy_units_count=1,
        ),
        plan,
    )

    assert payload["detected"] is False
    assert payload["reason"] == "planning_signal_without_execution_evidence"
    assert payload["planning_signal_present"] is True
    assert payload["friendly_combat_prerequisites_met"] is True
    assert payload["attack_order_near_enemy"] is True
    assert payload["execution_evidence_available"] is False
    assert payload["rally_eligible"] is False
    assert payload["target_position"] == [90.0, 80.0]


def test_build_combat_event_payload_confirms_contact_after_execution_applied():
    plan = TacticalPlan(
        name="basic_attack_order",
        strategy="default",
        order="attack_order",
        reason="army_threshold_met_with_known_enemy_start",
        attack_reason="army_threshold_met_with_known_enemy_start",
        order_prerequisites_met=True,
        target_position=(90.0, 80.0),
        own_army_count=4,
    )
    payload = build_combat_event_payload(
        GameState(
            game_loop=4000,
            game_time=180.0,
            known_enemy_start_location=(90.0, 80.0),
            own_army_count=4,
            visible_enemy_units_count=1,
        ),
        plan,
        execution_context={
            "outcome": "applied",
            "execution_reason": "attack_order_command_applied",
            "applied_command_count": 4,
            "execution_army_count": 4,
            "execution_idle_army_count": 2,
            "execution_army_source": "self_units_combat_fallback",
        },
    )

    assert payload["detected"] is True
    assert payload["reason"] == "execution_applied_with_enemy_contact"
    assert payload["execution_evidence_available"] is True
    assert payload["execution_outcome"] == "applied"
    assert payload["execution_reason"] == "attack_order_command_applied"
    assert payload["execution_applied_count"] == 4


def test_build_combat_event_payload_has_structured_no_combat_reason():
    plan = TacticalPlan(
        name="basic_army_rally",
        strategy="default",
        order="army_rally",
        reason="waiting_for_attack_or_defend_condition",
        regroup_reason="waiting_for_attack_or_defend_condition",
        rally_eligible=False,
        order_prerequisites_met=True,
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
    assert payload["rally_eligible"] is False


def test_tactical_manager_rallies_when_enemy_start_unknown_even_after_threshold():
    plan = TacticalManager(
        BuildOrderConfig(attack_army_supply_threshold=4, attack_game_time_threshold=999.0)
    ).plan(
        GameState(
            game_loop=0,
            game_time=120.0,
            own_start_location=(10.0, 20.0),
            known_enemy_start_location=None,
            own_army_count=4,
        ),
        StrategyDecision("default"),
    )

    assert plan.order == "army_rally"
    assert plan.regroup_reason == "known_enemy_start_location_missing"
    assert plan.order_prerequisites_met is True
