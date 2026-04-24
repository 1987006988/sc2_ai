"""Tactical manager skeleton."""

from sc2bot.config.schema import BuildOrderConfig
from sc2bot.domain.decisions import StrategyDecision, TacticalPlan
from sc2bot.domain.game_state import GameState


def build_combat_event_payload(state: GameState, plan: TacticalPlan) -> dict[str, object]:
    """Build minimal combat-event telemetry from visible state and tactical order."""

    enemy_combat_unit_nearby = state.visible_enemy_units_count > 0
    own_army_near_enemy = state.own_army_count > 0 and (
        state.visible_enemy_units_count > 0 or state.visible_enemy_structures_count > 0
    )
    attack_order_near_enemy = (
        state.own_army_count > 0
        and plan.order == "attack_order"
        and plan.target_position is not None
    )
    detected = (
        enemy_combat_unit_nearby or own_army_near_enemy or attack_order_near_enemy
    )
    if detected:
        reason = "combat_signal_detected"
    elif state.own_army_count <= 0:
        reason = "no_own_army_available"
    elif state.visible_enemy_units_count <= 0 and state.visible_enemy_structures_count <= 0:
        reason = "no_enemy_contact"
    else:
        reason = "no_combat_signal"
    return {
        "detected": detected,
        "reason": reason,
        "enemy_combat_unit_nearby": enemy_combat_unit_nearby,
        "own_army_near_enemy": own_army_near_enemy,
        "attack_order_near_enemy": attack_order_near_enemy,
        "army_order": plan.order,
        "army_order_reason": plan.reason,
        "rally_eligible": plan.rally_eligible,
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
                rally_eligible=False,
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
                rally_eligible=False,
                rally_point=rally_point,
                target_position=state.own_start_location,
                own_army_count=state.own_army_count,
                visible_enemy_units_count=state.visible_enemy_units_count,
            )
        if (
            state.own_army_count >= self.build_order.attack_army_supply_threshold
            or (
                state.own_army_count > 0
                and state.game_time >= self.build_order.attack_game_time_threshold
            )
        ) and state.known_enemy_start_location is not None:
            return TacticalPlan(
                name="basic_attack_order",
                strategy=decision.name,
                tags=("attack_order",),
                order="attack_order",
                reason="army_or_time_threshold_met",
                rally_eligible=False,
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
            reason="waiting_for_attack_or_defend_condition",
            rally_eligible=True,
            rally_point=rally_point,
            target_position=rally_point,
            own_army_count=state.own_army_count,
            visible_enemy_units_count=state.visible_enemy_units_count,
        )

    def detect_combat_event(self, state: GameState, plan: TacticalPlan) -> dict[str, object]:
        return build_combat_event_payload(state, plan)
