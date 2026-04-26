"""Configured R7 bot arms with telemetry dump."""

from __future__ import annotations

import json
from pathlib import Path

import sc2
from sc2 import UnitTypeId
from sc2.unit import Unit

import bot.injector as injector
from bot.chat.chat_interface import ChatInterface
from bot.configuration.basic_configuration import BasicConfiguration
from bot.logic.logic_interface import LogicInterface
from bot.main import MyBot
from bot.model.unit_role import UnitRole
from bot.r7.configurations import (
    R7BaselineConfiguration,
    R7RuleAdvisorConfiguration,
    R7WorldAdvisorConfiguration,
)
from bot.services.action_service import ActionService
from bot.services.debug_service import DebugService
from bot.services.eco_balance_service import EcoBalanceService
from bot.services.pathing_service import PathingService
from bot.services.role_service import RoleService
from bot.services.state_service import StateService
from bot.services.unit_type_service import UnitTypeService


class _R7ConfiguredBot(sc2.BotAI):
    with open(Path(__file__).parent.parent.parent / "botinfo.json") as f:
        NAME = json.load(f)["name"]

    CONFIG_CLS = BasicConfiguration

    def __init__(self, telemetry_path: str | None = None):
        config = self.CONFIG_CLS()
        injector.injector.init(config, self)
        from bot.hooks import hooks

        self.hooks = hooks
        self.chat: ChatInterface = injector.inject(ChatInterface)
        self.logic: LogicInterface = injector.inject(LogicInterface)
        self.state_service: StateService = injector.inject(StateService)
        self.action_service: ActionService = injector.inject(ActionService)
        self.role_service: RoleService = injector.inject(RoleService)
        self.debug_service: DebugService = injector.inject(DebugService)
        self.eco_balance: EcoBalanceService = injector.inject(EcoBalanceService)
        self.unit_type: UnitTypeService = injector.inject(UnitTypeService)
        self.pathing_service: PathingService = injector.inject(PathingService)
        self.r7_telemetry_path = Path(telemetry_path).expanduser() if telemetry_path else None
        super().__init__()

    async def on_unit_destroyed(self, unit_tag):
        self.hooks.call("on_unit_destroyed", unit_tag)
        if unit_tag in self.role_service.tags:
            self.role_service.removeTag(unit_tag)

    async def on_unit_created(self, unit: Unit):
        self.hooks.call("on_unit_created", unit)

    async def on_building_construction_complete(self, unit):
        self.hooks.call("on_building_construction_complete", unit)

    async def saturate_gas(self, unit: Unit):
        actions = []
        for drone in self.units(UnitTypeId.DRONE).closer_than(15, unit.position).take(3, require_all=False):
            actions.append(drone.gather(unit))
        await self.do_actions(actions)

    async def on_step(self, iteration):
        if iteration == 0:
            await self.do(self.units(UnitTypeId.LARVA).random.train(UnitTypeId.DRONE))
            await self.worker_split()
            self.state_service.on_first_iteration()
            self.hooks.call("on_init")
            self.logic.on_init()
        self.eco_balance.init_step()
        self.state_service.update()
        self.pathing_service.update()
        await self.chat.on_step(iteration)
        await self.logic.on_step(iteration)
        actions = self.action_service.get_all()
        await self.do_actions(actions)
        self.action_service.clear()
        self.state_service.previous_iter_own_units = self.state_service.own_units

    async def worker_split(self):
        for worker in self.workers:
            closest_mineral_patch = self.state.mineral_field.closest_to(worker)
            await self.do(worker.gather(closest_mineral_patch))

    def on_end(self, game_result):
        if not self.r7_telemetry_path:
            return
        self.r7_telemetry_path.parent.mkdir(parents=True, exist_ok=True)
        stats = getattr(self.state_service, "r7_advisor_stats", {})
        payload = {
            "result": str(game_result),
            "game_time": self.state_service.getTimeInSeconds() if hasattr(self, "state_service") else 0.0,
            "mode": getattr(self.state_service, "mode", "unknown"),
            "own_townhalls_count": getattr(self.state_service.own_townhalls, "amount", 0),
            "enemy_townhalls_count": getattr(self.state_service.enemy_townhalls, "amount", 0),
            "own_army_count": getattr(self.state_service.own_army_units, "amount", 0),
            "enemy_army_count": getattr(self.state_service.enemy_army_units, "amount", 0),
            "own_army_value": float(getattr(self.state_service, "own_army_value", 0.0)),
            "enemy_army_value": float(getattr(self.state_service, "enemy_army_value", 0.0)),
            "drone_count": int(getattr(self.state_service, "drone_count", 0)),
            "scouting_information": sorted(
                info.name for info in getattr(self.state_service, "scouting_information", ())
            ),
            "advisor_stats": stats,
        }
        self.r7_telemetry_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class R7BaselineBot(_R7ConfiguredBot):
    CONFIG_CLS = R7BaselineConfiguration


class R7RuleAdvisorBot(_R7ConfiguredBot):
    CONFIG_CLS = R7RuleAdvisorConfiguration


class R7WorldAdvisorBot(_R7ConfiguredBot):
    CONFIG_CLS = R7WorldAdvisorConfiguration
