"""R7 advisor-aware spending wrappers for sludge-revived."""

from __future__ import annotations

from sc2 import UnitTypeId

import bot.injector as injector
from bot.logic.spending.spending_v2 import Spendingv2
from bot.model.unit_type_abstraction import UnitTypeAbstraction
from bot.r7.macro_advisor import (
    RuleMacroAdvisor,
    WorldModelRuntime,
    build_state_snapshot,
    response_from_prediction,
)
from bot.r7.runtime_state import world_model_path
from bot.services.state_service import StateService


class _R7AdvisorSpendingBase(Spendingv2):
    def __init__(self):
        super().__init__()
        self.state: StateService = injector.inject(StateService)
        self._advisor = self._build_advisor()

    def _build_advisor(self):
        raise NotImplementedError

    def get_current_priorities(self):
        priorities = super().get_current_priorities()
        state, observation = build_state_snapshot(self.state)
        prediction = self._advisor.predict(state, observation)
        response = response_from_prediction(state, observation, prediction)
        self._apply_response(response, priorities)
        return priorities

    def _ensure_r7_state(self) -> None:
        if not hasattr(self.state, "r7_proxy_scout_target_count"):
            self.state.r7_proxy_scout_target_count = 4
        if not hasattr(self.state, "r7_advisor_stats"):
            self.state.r7_advisor_stats = {
                "advisor/applied_count": 0,
                "advisor/selected_macro_action_counts": {},
                "advisor/mode_override_counts": {},
                "advisor/priority_injection_counts": {},
                "advisor/proxy_scout_target_max": 4,
                "advisor/last_response": {},
            }

    def _increment_count(self, bucket: str, key: str) -> None:
        target = self.state.r7_advisor_stats[bucket]
        target[key] = int(target.get(key, 0)) + 1

    def _apply_response(self, response, priorities) -> None:
        self._ensure_r7_state()
        self.state.r7_advisor_stats["advisor/applied_count"] += 1
        self.state.r7_advisor_stats["advisor/last_response"] = response.to_dict()
        self._increment_count(
            "advisor/selected_macro_action_counts",
            response.selected_macro_action,
        )
        self.state.r7_proxy_scout_target_count = response.proxy_scout_target_count
        self.state.r7_advisor_stats["advisor/proxy_scout_target_max"] = max(
            int(self.state.r7_advisor_stats["advisor/proxy_scout_target_max"]),
            int(response.proxy_scout_target_count),
        )

        if response.defensive_posture:
            self.state.update_mode("defend")
            self._increment_count("advisor/mode_override_counts", "defend")
        elif response.force_attack_mode:
            self.state.update_mode("attack")
            self._increment_count("advisor/mode_override_counts", "attack")

        if response.production_tempo_delta >= 1:
            priorities.enqueue(UnitTypeAbstraction.ARMY, 35)
            if (
                self.state.drone_count >= 30
                and self.state.own_townhalls.amount < 4
                and self.state.own_army_units.amount >= 8
            ):
                priorities.enqueue(UnitTypeId.HATCHERY, 10020)
                self._increment_count("advisor/priority_injection_counts", "hatchery")
        if response.production_tempo_delta >= 2:
            priorities.enqueue(UnitTypeAbstraction.ARMY, 40)
            self._increment_count("advisor/priority_injection_counts", "army")

        if response.force_add_tech:
            can_start_lair = (
                self.state.drone_count >= 28
                and self.state.own_townhalls.amount >= 2
                and self.state.own_army_units.amount >= 8
            )
            can_add_hydra_den = (
                self.state.drone_count >= 34
                and self.state.own_townhalls.amount >= 3
                and self.state.own_army_units.amount >= 10
            )
            if (
                can_start_lair
                and self.state.get_unit_count(UnitTypeId.LAIR) < 1
                and self.state.get_unit_count(UnitTypeId.HIVE) < 1
            ):
                priorities.enqueue(UnitTypeId.LAIR, 10018)
                self._increment_count("advisor/priority_injection_counts", "lair")
            elif can_add_hydra_den and self.state.get_unit_count(UnitTypeId.HYDRALISKDEN) < 1:
                priorities.enqueue(UnitTypeId.HYDRALISKDEN, 10017)
                self._increment_count("advisor/priority_injection_counts", "hydraliskden")


class R7RuleAdvisorSpending(_R7AdvisorSpendingBase):
    def _build_advisor(self):
        return RuleMacroAdvisor()


class R7WorldAdvisorSpending(_R7AdvisorSpendingBase):
    def _build_advisor(self):
        return WorldModelRuntime(world_model_path())
