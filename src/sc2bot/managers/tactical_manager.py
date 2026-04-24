"""Tactical manager skeleton."""

from sc2bot.config.schema import BuildOrderConfig
from sc2bot.domain.decisions import StrategyDecision, TacticalPlan
from sc2bot.domain.game_state import GameState


def build_combat_event_payload(state: GameState, plan: TacticalPlan) -> dict[str, object]:
    """Build conservative combat-event telemetry from visible state and tactical plan.

    The payload intentionally separates:
    - plan emission / tactical intent
    - combat prerequisites
    - executed friendly-combat evidence

    Planning or visibility signals alone must not be recorded as executed
    friendly combat.
    """

    enemy_contact_visible = (
        state.visible_enemy_units_count > 0 or state.visible_enemy_structures_count > 0
    )
    enemy_combat_unit_nearby = state.visible_enemy_units_count > 0
    combat_capable_order_emitted = plan.order in {"defend_order", "attack_order"}
    planning_signal_present = combat_capable_order_emitted
    tactical_prerequisites_met = (
        state.own_army_count > 0
        and combat_capable_order_emitted
        and plan.order_prerequisites_met
    )
    own_army_near_enemy = tactical_prerequisites_met and enemy_contact_visible
    attack_order_near_enemy = (
        tactical_prerequisites_met
        and plan.order == "attack_order"
        and plan.target_position is not None
        and enemy_contact_visible
    )
    friendly_combat_prerequisites_met = own_army_near_enemy
    execution_evidence_available = plan.execution_evidence != "planning_only"
    detected = friendly_combat_prerequisites_met and execution_evidence_available
    if detected:
        reason = "friendly_combat_execution_confirmed"
    elif state.own_army_count <= 0:
        reason = "no_own_army_available"
    elif not combat_capable_order_emitted:
        reason = "no_combat_capable_order_emitted"
    elif not enemy_contact_visible:
        reason = "no_enemy_contact"
    elif not plan.order_prerequisites_met:
        reason = "combat_order_prerequisites_not_met"
    else:
        reason = "planning_signal_without_execution_evidence"
    return {
        "detected": detected,
        "reason": reason,
        "planning_signal_present": planning_signal_present,
        "combat_capable_order_emitted": combat_capable_order_emitted,
        "tactical_prerequisites_met": tactical_prerequisites_met,
        "friendly_combat_prerequisites_met": friendly_combat_prerequisites_met,
        "execution_evidence_available": execution_evidence_available,
        "enemy_combat_unit_nearby": enemy_combat_unit_nearby,
        "enemy_contact_visible": enemy_contact_visible,
        "own_army_near_enemy": own_army_near_enemy,
        "attack_order_near_enemy": attack_order_near_enemy,
        "army_order": plan.order,
        "army_order_reason": plan.reason,
        "defend_reason": plan.defend_reason,
        "attack_reason": plan.attack_reason,
        "regroup_reason": plan.regroup_reason,
        "rally_eligible": plan.rally_eligible,
        "order_prerequisites_met": plan.order_prerequisites_met,
        "execution_evidence": plan.execution_evidence,
        "own_army_count": state.own_army_count,
        "visible_enemy_units_count": state.visible_enemy_units_count,
        "visible_enemy_structures_count": state.visible_enemy_structures_count,
        "target_position": list(plan.target_position) if plan.target_position else None,
        "game_loop": state.game_loop,
        "game_time": state.game_time,
    }


class TacticalManager:
    """Turns strategy decisions into army-level tactical plans."""

    def __init__(self, build_order: BuildOrderConfig | None = None) -> None:
        self.build_order = build_order or BuildOrderConfig()

    def plan(self, state: GameState, decision: StrategyDecision) -> TacticalPlan:
        rally_point = state.own_start_location
        if state.own_army_count <= 0:
            return TacticalPlan(
                name="hold_no_army",
                strategy=decision.name,
                tags=("no_army",),
                order="hold_position",
                reason="no_army_available",
                regroup_reason="no_army_available",
                rally_eligible=False,
                order_prerequisites_met=False,
                rally_point=rally_point,
                target_position=rally_point,
                own_army_count=state.own_army_count,
                visible_enemy_units_count=state.visible_enemy_units_count,
            )
        if state.visible_enemy_units_count > 0:
            return TacticalPlan(
                name="basic_defend_order",
                strategy=decision.name,
                tags=("defend_order",),
                order="defend_order",
                reason="enemy_units_visible_near_base",
                defend_reason="enemy_units_visible_near_base",
                rally_eligible=False,
                order_prerequisites_met=True,
                rally_point=rally_point,
                target_position=state.own_start_location,
                own_army_count=state.own_army_count,
                visible_enemy_units_count=state.visible_enemy_units_count,
            )
        attack_threshold_by_army = (
            state.own_army_count >= self.build_order.attack_army_supply_threshold
        )
        attack_threshold_by_time = (
            state.own_army_count > 0
            and state.game_time >= self.build_order.attack_game_time_threshold
        )
        if state.known_enemy_start_location is None:
            regroup_reason = "known_enemy_start_location_missing"
        elif attack_threshold_by_army:
            regroup_reason = "waiting_for_attack_contact_after_army_threshold"
        elif attack_threshold_by_time:
            regroup_reason = "waiting_for_attack_contact_after_time_threshold"
        else:
            regroup_reason = "waiting_for_attack_or_defend_condition"
        if (
            attack_threshold_by_army or attack_threshold_by_time
        ) and state.known_enemy_start_location is not None:
            attack_reason = (
                "army_threshold_met_with_known_enemy_start"
                if attack_threshold_by_army
                else "time_threshold_met_with_known_enemy_start"
            )
            return TacticalPlan(
                name="basic_attack_order",
                strategy=decision.name,
                tags=("attack_order",),
                order="attack_order",
                reason=attack_reason,
                attack_reason=attack_reason,
                rally_eligible=False,
                order_prerequisites_met=True,
                rally_point=rally_point,
                target_position=state.known_enemy_start_location,
                own_army_count=state.own_army_count,
                visible_enemy_units_count=state.visible_enemy_units_count,
            )
        return TacticalPlan(
            name="basic_army_rally",
            strategy=decision.name,
            tags=("army_rally",),
            order="army_rally",
            reason=regroup_reason,
            regroup_reason=regroup_reason,
            rally_eligible=True,
            order_prerequisites_met=True,
            rally_point=rally_point,
            target_position=rally_point,
            own_army_count=state.own_army_count,
            visible_enemy_units_count=state.visible_enemy_units_count,
        )

    def detect_combat_event(self, state: GameState, plan: TacticalPlan) -> dict[str, object]:
        return build_combat_event_payload(state, plan)
