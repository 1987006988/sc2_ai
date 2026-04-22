"""Minimal manager call order for the bot skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from sc2bot.config.schema import BuildOrderConfig, RuntimeConfig
from sc2bot.domain.decisions import StrategyResponse
from sc2bot.domain.game_state import GameState
from sc2bot.runtime.dependency_container import DependencyContainer

if TYPE_CHECKING:
    from sc2.bot_ai import BotAI

DEFAULT_SUSTAIN_UNTIL_GAME_LOOP = 2600
GATEWAY_MINERALS = 150
ASSIMILATOR_MINERALS = 75
CYBERNETICS_CORE_MINERALS = 150
ZEALOT_MINERALS = 100
STALKER_MINERALS = 125
STALKER_VESPENE = 50
_TOWNHALL_TYPE_NAMES = {
    "COMMANDCENTER",
    "HATCHERY",
    "LAIR",
    "HIVE",
    "NEXUS",
    "ORBITALCOMMAND",
    "PLANETARYFORTRESS",
}


@dataclass
class GameLoop:
    container: DependencyContainer
    _last_strategy_response_key: tuple[str, str] | None = None

    def process_state(self, state: GameState) -> StrategyResponse:
        observations = self.container.scouting.update(state)
        prediction = self.container.opponent_model.predict(observations)
        decision = self.container.strategy.decide(state, prediction)
        strategy_response = self.container.strategy.select_response(
            prediction, self.container.opponent_model_config
        )
        self.container.macro.update(state, decision)
        tactical_plan = self.container.tactical.plan(state, decision)
        self.container.micro.execute(state, tactical_plan)
        self.container.telemetry.record("game_state", state.to_dict())
        self.container.telemetry.record("army_order", tactical_plan.to_dict())
        combat_event = self.container.tactical.detect_combat_event(state, tactical_plan)
        self.container.telemetry.record(
            "combat_event_detected" if combat_event["detected"] else "combat_event_skipped",
            combat_event,
        )
        self.container.telemetry.record(
            "opponent_prediction",
            {
                "opponent_model_mode": self.container.opponent_model_mode,
                "prediction": prediction.to_dict(),
            },
        )
        self.container.telemetry.record(
            "strategy_decision",
            {
                "decision": decision.name,
                "opponent_model": prediction.model_name,
                "opponent_model_mode": self.container.opponent_model_mode,
                "prediction_mode": prediction.prediction_mode,
                "prediction_signals": list(prediction.signals),
            },
        )
        self.container.telemetry.record("strategy_response", strategy_response.to_dict())
        response_key = (
            strategy_response.selected_response_tag,
            strategy_response.strategy_switch_reason,
        )
        if response_key != self._last_strategy_response_key:
            self._last_strategy_response_key = response_key
            self.container.telemetry.record("strategy_switch", strategy_response.to_dict())
        return strategy_response

    def step(self) -> None:
        self.process_state(GameState.empty())


def build_game_state_from_bot_ai(bot_ai: "BotAI") -> GameState:
    """Convert a live python-sc2 bot snapshot into the project's GameState."""

    enemy_units = tuple(sorted(_unit_type_name(unit) for unit in getattr(bot_ai, "enemy_units", [])))
    enemy_structures = tuple(
        sorted(_unit_type_name(unit) for unit in getattr(bot_ai, "enemy_structures", []))
    )
    game_loop = int(getattr(bot_ai.state, "game_loop", 0))
    game_time = float(getattr(bot_ai, "time", game_loop / 22.4))
    return GameState(
        game_loop=game_loop,
        game_time=game_time,
        own_race=_race_name(getattr(bot_ai, "race", None)),
        enemy_race=_race_name(getattr(bot_ai, "enemy_race", None)),
        own_start_location=_position_tuple(getattr(bot_ai, "start_location", None)),
        known_enemy_start_location=_first_position_tuple(
            getattr(bot_ai, "enemy_start_locations", [])
        ),
        visible_enemy_units_count=len(enemy_units),
        visible_enemy_structures_count=len(enemy_structures),
        visible_enemy_units=enemy_units,
        visible_enemy_structures=enemy_structures,
        visible_enemy_townhalls_count=sum(
            1 for name in enemy_structures if name.upper() in _TOWNHALL_TYPE_NAMES
        ),
        own_workers_count=len(getattr(bot_ai, "workers", [])),
        own_army_count=len(getattr(bot_ai, "army", [])),
        own_townhalls_count=len(getattr(bot_ai, "townhalls", [])),
        minerals=int(getattr(bot_ai, "minerals", 0)),
        vespene=int(getattr(bot_ai, "vespene", 0)),
        supply_used=int(getattr(bot_ai, "supply_used", 0)),
        supply_cap=int(getattr(bot_ai, "supply_cap", 0)),
    )


def _unit_type_name(unit: Any) -> str:
    type_id = getattr(unit, "type_id", None)
    return str(getattr(type_id, "name", type_id or "unknown")).lower()


def _race_name(race: Any) -> str:
    return str(getattr(race, "name", race or "unknown")).lower()


def _position_tuple(position: Any) -> tuple[float, float] | None:
    if position is None:
        return None
    x = getattr(position, "x", None)
    y = getattr(position, "y", None)
    if x is None or y is None:
        return None
    return (float(x), float(y))


def _first_position_tuple(positions: Any) -> tuple[float, float] | None:
    try:
        first = next(iter(positions))
    except StopIteration:
        return None
    except TypeError:
        return None
    return _position_tuple(first)


def should_leave_after_sustain_limit(
    game_loop: int, sustain_until_game_loop: int = DEFAULT_SUSTAIN_UNTIL_GAME_LOOP
) -> bool:
    """Return whether the minimal sustained runtime window has elapsed."""

    return game_loop >= sustain_until_game_loop


def build_supply_sustain_payload(
    reason: str,
    supply_used: int,
    supply_cap: int,
    runtime: RuntimeConfig,
) -> dict[str, object]:
    """Build the structured telemetry payload for supply sustain events."""

    return {
        "reason": reason,
        "supply_used": int(supply_used),
        "supply_cap": int(supply_cap),
        "threshold": runtime.supply_sustain_threshold,
        "structure": runtime.supply_structure_name,
    }


def gateway_build_skip_reason(
    state: GameState,
    build_order: BuildOrderConfig,
    *,
    pending_gateway_count: int = 0,
    existing_gateway_count: int = 0,
) -> str | None:
    """Return a structured skip reason, or None when Gateway should be attempted."""

    if existing_gateway_count > 0:
        return "gateway_already_exists"
    if pending_gateway_count > 0:
        return "gateway_already_pending"
    if state.own_workers_count <= 0:
        return "no_worker_available"
    if state.minerals < GATEWAY_MINERALS:
        return "insufficient_minerals"
    if state.own_workers_count < build_order.gateway_min_probe_count:
        return "insufficient_probe_count"
    if state.game_time < build_order.gateway_min_game_time:
        return "gateway_timing_not_reached"
    return None


def build_gateway_build_payload(
    reason: str,
    state: GameState,
    build_order: BuildOrderConfig,
    *,
    pending_gateway_count: int = 0,
    existing_gateway_count: int = 0,
) -> dict[str, object]:
    """Build stable telemetry for Phase B Gateway build events."""

    return {
        "reason": reason,
        "structure": "gateway",
        "game_loop": state.game_loop,
        "game_time": state.game_time,
        "minerals": state.minerals,
        "own_workers_count": state.own_workers_count,
        "gateway_min_probe_count": build_order.gateway_min_probe_count,
        "gateway_min_game_time": build_order.gateway_min_game_time,
        "pending_gateway_count": pending_gateway_count,
        "existing_gateway_count": existing_gateway_count,
    }


def assimilator_build_skip_reason(
    state: GameState,
    build_order: BuildOrderConfig,
    *,
    gateway_ready_count: int = 0,
    pending_assimilator_count: int = 0,
    existing_assimilator_count: int = 0,
) -> str | None:
    """Return a structured skip reason, or None when Assimilator should be attempted."""

    if not build_order.assimilator_enabled:
        return "assimilator_disabled"
    if existing_assimilator_count > 0:
        return "assimilator_already_exists"
    if pending_assimilator_count > 0:
        return "assimilator_already_pending"
    if gateway_ready_count <= 0:
        return "gateway_not_ready"
    if state.own_workers_count <= 0:
        return "no_worker_available"
    if state.minerals < ASSIMILATOR_MINERALS:
        return "insufficient_minerals"
    return None


def cybernetics_core_build_skip_reason(
    state: GameState,
    build_order: BuildOrderConfig,
    *,
    gateway_ready_count: int = 0,
    pending_cybernetics_core_count: int = 0,
    existing_cybernetics_core_count: int = 0,
) -> str | None:
    """Return a structured skip reason, or None when Cybernetics Core should be attempted."""

    if not build_order.cybernetics_core_enabled:
        return "cybernetics_core_disabled"
    if existing_cybernetics_core_count > 0:
        return "cybernetics_core_already_exists"
    if pending_cybernetics_core_count > 0:
        return "cybernetics_core_already_pending"
    if gateway_ready_count <= 0:
        return "gateway_not_ready"
    if state.own_workers_count <= 0:
        return "no_worker_available"
    if state.minerals < CYBERNETICS_CORE_MINERALS:
        return "insufficient_minerals"
    return None


def build_tech_structure_payload(
    reason: str,
    structure: str,
    state: GameState,
    *,
    gateway_ready_count: int = 0,
    pending_count: int = 0,
    existing_count: int = 0,
) -> dict[str, object]:
    """Build stable telemetry for Phase B post-Gateway tech structure events."""

    return {
        "reason": reason,
        "structure": structure,
        "game_loop": state.game_loop,
        "game_time": state.game_time,
        "minerals": state.minerals,
        "vespene": state.vespene,
        "own_workers_count": state.own_workers_count,
        "gateway_ready_count": gateway_ready_count,
        "pending_count": pending_count,
        "existing_count": existing_count,
    }


def combat_unit_production_skip_reason(
    state: GameState,
    unit_name: str,
    *,
    gateway_ready_count: int = 0,
    cybernetics_core_ready_count: int = 0,
) -> str | None:
    """Return a structured skip reason, or None when the combat unit can be trained."""

    if gateway_ready_count <= 0:
        return "gateway_not_ready"
    if unit_name == "zealot":
        if state.minerals < ZEALOT_MINERALS:
            return "insufficient_minerals"
        return None
    if unit_name == "stalker":
        if cybernetics_core_ready_count <= 0:
            return "cybernetics_core_not_ready"
        if state.minerals < STALKER_MINERALS:
            return "insufficient_minerals"
        if state.vespene < STALKER_VESPENE:
            return "insufficient_vespene"
        return None
    return "unsupported_combat_unit"


def select_combat_unit_for_production(
    state: GameState,
    build_order: BuildOrderConfig,
    *,
    gateway_ready_count: int = 0,
    cybernetics_core_ready_count: int = 0,
) -> tuple[str | None, str | None]:
    """Select a minimal combat unit to train, returning (unit_name, skip_reason)."""

    ordered_units = sorted(
        (
            ("zealot", build_order.zealot_production_priority),
            ("stalker", build_order.stalker_production_priority),
        ),
        key=lambda item: item[1],
    )
    fallback_reason = "no_supported_combat_unit"
    for unit_name, _priority in ordered_units:
        reason = combat_unit_production_skip_reason(
            state,
            unit_name,
            gateway_ready_count=gateway_ready_count,
            cybernetics_core_ready_count=cybernetics_core_ready_count,
        )
        if reason is None:
            return unit_name, None
        if fallback_reason == "no_supported_combat_unit":
            fallback_reason = reason
    return None, fallback_reason


def build_combat_unit_production_payload(
    reason: str,
    unit_name: str | None,
    state: GameState,
    *,
    gateway_ready_count: int = 0,
    cybernetics_core_ready_count: int = 0,
    idle_gateway_count: int = 0,
) -> dict[str, object]:
    """Build stable telemetry for Phase B combat-unit production events."""

    return {
        "reason": reason,
        "unit": unit_name or "none",
        "game_loop": state.game_loop,
        "game_time": state.game_time,
        "minerals": state.minerals,
        "vespene": state.vespene,
        "supply_used": state.supply_used,
        "supply_cap": state.supply_cap,
        "gateway_ready_count": gateway_ready_count,
        "cybernetics_core_ready_count": cybernetics_core_ready_count,
        "idle_gateway_count": idle_gateway_count,
    }


def build_minimal_behavior_intervention_payload(
    response: StrategyResponse,
    *,
    action: str,
    outcome: str,
    reason: str,
) -> dict[str, object]:
    """Build structured telemetry for Phase 1E minimal behavior hooks."""

    return {
        "action": action,
        "outcome": outcome,
        "reason": reason,
        "selected_response_tag": response.selected_response_tag,
        "strategy_switch_reason": response.strategy_switch_reason,
        "intervention_mode": response.intervention_mode,
    }


def record_minimal_behavior_intervention(
    telemetry: Any,
    response: StrategyResponse,
    *,
    action: str,
    outcome: str,
    reason: str,
) -> None:
    telemetry.record(
        "minimal_behavior_intervention",
        build_minimal_behavior_intervention_payload(
            response,
            action=action,
            outcome=outcome,
            reason=reason,
        ),
    )


def should_apply_minimal_behavior(response: StrategyResponse) -> bool:
    return response.intervention_mode == "minimal_behavior"


def build_python_sc2_local_bot(
    container: DependencyContainer,
    bot_name: str,
    runtime: RuntimeConfig | None = None,
    build_order: BuildOrderConfig | None = None,
) -> Any:
    """Build a minimal python-sc2 BotAI for sustained local match validation."""

    from sc2.bot_ai import BotAI
    from sc2.ids.unit_typeid import UnitTypeId

    runtime_config = runtime or RuntimeConfig(max_game_loop=DEFAULT_SUSTAIN_UNTIL_GAME_LOOP)
    build_order_config = build_order or BuildOrderConfig()
    game_loop = GameLoop(container)

    class ProjectBotAI(BotAI):
        _scout_worker_tag: int | None = None

        async def on_start(self) -> None:
            container.telemetry.record(
                "sc2_match_started",
                {
                    "bot": bot_name,
                    "opponent_model_mode": container.opponent_model_mode,
                    "max_game_loop": runtime_config.max_game_loop,
                    "max_steps": runtime_config.max_steps,
                },
            )

        async def on_step(self, iteration: int) -> None:
            try:
                state = build_game_state_from_bot_ai(self)
                strategy_response = game_loop.process_state(state)
                await self._execute_survival_baseline(strategy_response)
                exit_reason = self._exit_reason(iteration, state)
                if exit_reason:
                    container.runtime_exit_reason = exit_reason
                    container.telemetry.record(
                        "sc2_match_exit_requested",
                        {
                            "reason": exit_reason,
                            "iteration": iteration,
                            "game_loop": state.game_loop,
                            "max_game_loop": runtime_config.max_game_loop,
                            "max_steps": runtime_config.max_steps,
                        },
                    )
                    await self.client.leave()
            except Exception as exc:
                container.runtime_exit_reason = "gameplay_error"
                container.telemetry.record(
                    "gameplay_error",
                    {"iteration": iteration, "error": str(exc)},
                )
                await self.client.leave()

        def _exit_reason(self, iteration: int, state: GameState) -> str | None:
            if runtime_config.max_steps is not None and iteration >= runtime_config.max_steps:
                return "max_steps_reached"
            if should_leave_after_sustain_limit(state.game_loop, runtime_config.max_game_loop):
                return "max_game_time_reached"
            return None

        async def _execute_survival_baseline(self, strategy_response: StrategyResponse) -> None:
            if runtime_config.worker_gather:
                await self._safe_worker_gather()
            if runtime_config.worker_scout:
                await self._safe_worker_scout(strategy_response)
            if runtime_config.supply_sustain:
                await self._safe_supply_sustain()
            await self._safe_gateway_build()
            await self._safe_assimilator_build()
            await self._safe_cybernetics_core_build()
            await self._safe_combat_unit_production()
            if runtime_config.worker_production:
                await self._safe_worker_production()
            if runtime_config.army_defense:
                await self._safe_army_defense(strategy_response)

        async def _safe_worker_gather(self) -> None:
            if not self.mineral_field:
                return
            for worker in self.workers.idle:
                if self._scout_worker_tag is not None and worker.tag == self._scout_worker_tag:
                    continue
                target = self.mineral_field.closest_to(worker)
                worker.gather(target)

        async def _safe_worker_scout(self, strategy_response: StrategyResponse) -> None:
            if (
                should_apply_minimal_behavior(strategy_response)
                and strategy_response.selected_response_tag == "continue_scouting"
            ):
                record_minimal_behavior_intervention(
                    container.telemetry,
                    strategy_response,
                    action="scout_persistence",
                    outcome="active",
                    reason="continue_scouting",
                )
            if self._scout_worker_tag is not None:
                return
            if not self.workers or not self.enemy_start_locations:
                return
            worker = self.workers.first
            self._scout_worker_tag = worker.tag
            worker.move(self.enemy_start_locations[0])
            container.telemetry.record(
                "worker_scout_dispatched",
                {"worker_tag": worker.tag, "target": list(_position_tuple(self.enemy_start_locations[0]) or ())},
            )

        async def _safe_worker_production(self) -> None:
            worker_type = self._worker_type()
            if worker_type is None or not self.can_afford(worker_type):
                return
            for townhall in self.townhalls.ready.idle:
                townhall.train(worker_type)
                return

        async def _safe_supply_sustain(self) -> None:
            if runtime_config.supply_structure_name.lower() != "pylon":
                self._record_supply_sustain("skipped", "unsupported_supply_structure")
                return
            supply_left = int(getattr(self, "supply_cap", 0)) - int(
                getattr(self, "supply_used", 0)
            )
            if supply_left > runtime_config.supply_sustain_threshold:
                return
            pylon_type = UnitTypeId.PYLON
            if self.already_pending(pylon_type):
                self._record_supply_sustain("skipped", "pylon_already_pending")
                return
            if not self.can_afford(pylon_type):
                self._record_supply_sustain("skipped", "insufficient_minerals")
                return
            if not self.workers:
                self._record_supply_sustain("skipped", "no_worker_available")
                return
            if not self.townhalls:
                self._record_supply_sustain("skipped", "no_townhall_available")
                return
            near = self.townhalls.ready.first.position
            map_center = getattr(getattr(self, "game_info", None), "map_center", None)
            if map_center is not None:
                near = near.towards(map_center, 6)
            self._record_supply_sustain("attempt", "supply_near_cap")
            try:
                result = await self.build(
                    pylon_type,
                    near=near,
                    max_distance=12,
                    random_alternative=True,
                    placement_step=2,
                )
            except Exception as exc:
                self._record_supply_sustain("failed", f"build_exception:{exc}")
                return
            if result:
                self._record_supply_sustain("success", "build_command_issued")
            else:
                self._record_supply_sustain("failed", "placement_not_found")

        def _record_supply_sustain(self, outcome: str, reason: str) -> None:
            container.telemetry.record(
                f"supply_sustain_{outcome}",
                build_supply_sustain_payload(
                    reason=reason,
                    supply_used=int(getattr(self, "supply_used", 0)),
                    supply_cap=int(getattr(self, "supply_cap", 0)),
                    runtime=runtime_config,
                ),
            )

        async def _safe_gateway_build(self) -> None:
            gateway_type = UnitTypeId.GATEWAY
            pending_count = int(self.already_pending(gateway_type))
            existing_count = int(self.structures(gateway_type).amount)
            state = build_game_state_from_bot_ai(self)
            skip_reason = gateway_build_skip_reason(
                state,
                build_order_config,
                pending_gateway_count=pending_count,
                existing_gateway_count=existing_count,
            )
            if skip_reason:
                self._record_gateway_build(
                    "skipped",
                    skip_reason,
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )
                return
            if not self.townhalls:
                self._record_gateway_build(
                    "skipped",
                    "no_townhall_available",
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )
                return
            if not self.townhalls.ready:
                self._record_gateway_build(
                    "skipped",
                    "no_ready_townhall_available",
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )
                return
            near = self.townhalls.ready.first.position
            map_center = getattr(getattr(self, "game_info", None), "map_center", None)
            if map_center is not None:
                near = near.towards(map_center, 8)
            self._record_gateway_build(
                "attempt",
                "gateway_conditions_met",
                state,
                pending_gateway_count=pending_count,
                existing_gateway_count=existing_count,
            )
            try:
                result = await self.build(
                    gateway_type,
                    near=near,
                    max_distance=16,
                    random_alternative=True,
                    placement_step=2,
                )
            except Exception as exc:
                self._record_gateway_build(
                    "failed",
                    f"build_exception:{exc}",
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )
                return
            if result:
                self._record_gateway_build(
                    "success",
                    "build_command_issued",
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )
            else:
                self._record_gateway_build(
                    "failed",
                    "placement_not_found",
                    state,
                    pending_gateway_count=pending_count,
                    existing_gateway_count=existing_count,
                )

        def _record_gateway_build(
            self,
            outcome: str,
            reason: str,
            state: GameState,
            *,
            pending_gateway_count: int,
            existing_gateway_count: int,
        ) -> None:
            container.telemetry.record(
                f"gateway_build_{outcome}",
                build_gateway_build_payload(
                    reason,
                    state,
                    build_order_config,
                    pending_gateway_count=pending_gateway_count,
                    existing_gateway_count=existing_gateway_count,
                ),
            )

        async def _safe_assimilator_build(self) -> None:
            assimilator_type = UnitTypeId.ASSIMILATOR
            gateway_type = UnitTypeId.GATEWAY
            pending_count = int(self.already_pending(assimilator_type))
            existing_count = int(self.structures(assimilator_type).amount)
            gateway_ready_count = int(self.structures(gateway_type).ready.amount)
            state = build_game_state_from_bot_ai(self)
            skip_reason = assimilator_build_skip_reason(
                state,
                build_order_config,
                gateway_ready_count=gateway_ready_count,
                pending_assimilator_count=pending_count,
                existing_assimilator_count=existing_count,
            )
            if skip_reason:
                self._record_tech_structure_build(
                    "assimilator",
                    "skipped",
                    skip_reason,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            if not self.townhalls.ready:
                self._record_tech_structure_build(
                    "assimilator",
                    "skipped",
                    "no_ready_townhall_available",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            if not self.vespene_geyser:
                self._record_tech_structure_build(
                    "assimilator",
                    "skipped",
                    "no_geyser_available",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            geyser = self.vespene_geyser.closest_to(self.townhalls.ready.first)
            self._record_tech_structure_build(
                "assimilator",
                "attempt",
                "assimilator_conditions_met",
                state,
                gateway_ready_count=gateway_ready_count,
                pending_count=pending_count,
                existing_count=existing_count,
            )
            try:
                result = await self.build(assimilator_type, geyser)
            except Exception as exc:
                self._record_tech_structure_build(
                    "assimilator",
                    "failed",
                    f"build_exception:{exc}",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            if result:
                self._record_tech_structure_build(
                    "assimilator",
                    "success",
                    "build_command_issued",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
            else:
                self._record_tech_structure_build(
                    "assimilator",
                    "failed",
                    "placement_not_found",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )

        async def _safe_cybernetics_core_build(self) -> None:
            cybernetics_core_type = UnitTypeId.CYBERNETICSCORE
            gateway_type = UnitTypeId.GATEWAY
            pending_count = int(self.already_pending(cybernetics_core_type))
            existing_count = int(self.structures(cybernetics_core_type).amount)
            gateway_ready_count = int(self.structures(gateway_type).ready.amount)
            state = build_game_state_from_bot_ai(self)
            skip_reason = cybernetics_core_build_skip_reason(
                state,
                build_order_config,
                gateway_ready_count=gateway_ready_count,
                pending_cybernetics_core_count=pending_count,
                existing_cybernetics_core_count=existing_count,
            )
            if skip_reason:
                self._record_tech_structure_build(
                    "cybernetics_core",
                    "skipped",
                    skip_reason,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            if not self.townhalls.ready:
                self._record_tech_structure_build(
                    "cybernetics_core",
                    "skipped",
                    "no_ready_townhall_available",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            near = self.townhalls.ready.first.position
            map_center = getattr(getattr(self, "game_info", None), "map_center", None)
            if map_center is not None:
                near = near.towards(map_center, 10)
            self._record_tech_structure_build(
                "cybernetics_core",
                "attempt",
                "cybernetics_core_conditions_met",
                state,
                gateway_ready_count=gateway_ready_count,
                pending_count=pending_count,
                existing_count=existing_count,
            )
            try:
                result = await self.build(
                    cybernetics_core_type,
                    near=near,
                    max_distance=18,
                    random_alternative=True,
                    placement_step=2,
                )
            except Exception as exc:
                self._record_tech_structure_build(
                    "cybernetics_core",
                    "failed",
                    f"build_exception:{exc}",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
                return
            if result:
                self._record_tech_structure_build(
                    "cybernetics_core",
                    "success",
                    "build_command_issued",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )
            else:
                self._record_tech_structure_build(
                    "cybernetics_core",
                    "failed",
                    "placement_not_found",
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                )

        def _record_tech_structure_build(
            self,
            structure: str,
            outcome: str,
            reason: str,
            state: GameState,
            *,
            gateway_ready_count: int,
            pending_count: int,
            existing_count: int,
        ) -> None:
            container.telemetry.record(
                f"{structure}_build_{outcome}",
                build_tech_structure_payload(
                    reason,
                    structure,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    pending_count=pending_count,
                    existing_count=existing_count,
                ),
            )

        async def _safe_combat_unit_production(self) -> None:
            gateway_type = UnitTypeId.GATEWAY
            cybernetics_core_type = UnitTypeId.CYBERNETICSCORE
            gateway_ready_count = int(self.structures(gateway_type).ready.amount)
            cybernetics_core_ready_count = int(
                self.structures(cybernetics_core_type).ready.amount
            )
            idle_gateways = self.structures(gateway_type).ready.idle
            idle_gateway_count = int(idle_gateways.amount)
            state = build_game_state_from_bot_ai(self)
            unit_name, skip_reason = select_combat_unit_for_production(
                state,
                build_order_config,
                gateway_ready_count=gateway_ready_count,
                cybernetics_core_ready_count=cybernetics_core_ready_count,
            )
            if skip_reason:
                self._record_combat_unit_production(
                    "skipped",
                    skip_reason,
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                )
                return
            if not idle_gateways:
                self._record_combat_unit_production(
                    "skipped",
                    "no_idle_gateway",
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                )
                return
            unit_type = self._combat_unit_type(unit_name)
            if unit_type is None:
                self._record_combat_unit_production(
                    "skipped",
                    "unsupported_combat_unit",
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                )
                return
            if not self.can_afford(unit_type):
                self._record_combat_unit_production(
                    "skipped",
                    "cannot_afford_unit",
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                )
                return
            self._record_combat_unit_production(
                "attempt",
                "combat_unit_conditions_met",
                unit_name,
                state,
                gateway_ready_count=gateway_ready_count,
                cybernetics_core_ready_count=cybernetics_core_ready_count,
                idle_gateway_count=idle_gateway_count,
            )
            try:
                idle_gateways.first.train(unit_type)
            except Exception as exc:
                self._record_combat_unit_production(
                    "failed",
                    f"train_exception:{exc}",
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                )
                return
            self._record_combat_unit_production(
                "success",
                "train_command_issued",
                unit_name,
                state,
                gateway_ready_count=gateway_ready_count,
                cybernetics_core_ready_count=cybernetics_core_ready_count,
                idle_gateway_count=idle_gateway_count,
            )

        def _record_combat_unit_production(
            self,
            outcome: str,
            reason: str,
            unit_name: str | None,
            state: GameState,
            *,
            gateway_ready_count: int,
            cybernetics_core_ready_count: int,
            idle_gateway_count: int,
        ) -> None:
            container.telemetry.record(
                f"combat_unit_production_{outcome}",
                build_combat_unit_production_payload(
                    reason,
                    unit_name,
                    state,
                    gateway_ready_count=gateway_ready_count,
                    cybernetics_core_ready_count=cybernetics_core_ready_count,
                    idle_gateway_count=idle_gateway_count,
                ),
            )

        def _combat_unit_type(self, unit_name: str | None) -> Any:
            if unit_name == "zealot":
                return UnitTypeId.ZEALOT
            if unit_name == "stalker":
                return UnitTypeId.STALKER
            return None

        def _worker_type(self) -> Any:
            race_name = _race_name(getattr(self, "race", None))
            if race_name == "protoss":
                return UnitTypeId.PROBE
            if race_name == "terran":
                return UnitTypeId.SCV
            if race_name == "zerg":
                return UnitTypeId.DRONE
            return None

        async def _safe_army_defense(self, strategy_response: StrategyResponse) -> None:
            army = getattr(self, "army", None)
            if not army:
                if should_apply_minimal_behavior(strategy_response):
                    record_minimal_behavior_intervention(
                        container.telemetry,
                        strategy_response,
                        action="army_defense",
                        outcome="skipped",
                        reason="no_army_available",
                    )
                return
            defensive_posture = (
                should_apply_minimal_behavior(strategy_response)
                and strategy_response.selected_response_tag == "defensive_posture"
            )
            if defensive_posture:
                record_minimal_behavior_intervention(
                    container.telemetry,
                    strategy_response,
                    action="army_defense",
                    outcome="active",
                    reason="defensive_posture",
                )
                target = self.townhalls.ready.first.position if self.townhalls.ready else self.start_location
                for unit in army.idle:
                    unit.move(target)
                return
            if (
                should_apply_minimal_behavior(strategy_response)
                and strategy_response.selected_response_tag == "tech_alert"
            ):
                record_minimal_behavior_intervention(
                    container.telemetry,
                    strategy_response,
                    action="tech_alert",
                    outcome="telemetry_only",
                    reason="tech_alert",
                )
            if self.enemy_units:
                target = self.enemy_units.closest_to(self.start_location)
                for unit in army.idle:
                    unit.attack(target)
                return
            for unit in army.idle:
                unit.move(self.start_location)

    return ProjectBotAI()
