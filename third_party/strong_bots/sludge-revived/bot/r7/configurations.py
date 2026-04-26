"""R7 configuration classes for sludge-revived A/B/C arms."""

from __future__ import annotations

from bot.configuration.basic_configuration import BasicConfiguration
from bot.logic.logic_interface import LogicInterface
from bot.logic.spending.spending_interface import SpendingInterface
from bot.r7.spending import R7RuleAdvisorSpending, R7WorldAdvisorSpending


class R7BaselineConfiguration(BasicConfiguration):
    pass


class R7RuleAdvisorConfiguration(BasicConfiguration):
    def __init__(self):
        super().__init__()
        self.d[SpendingInterface] = R7RuleAdvisorSpending


class R7WorldAdvisorConfiguration(BasicConfiguration):
    def __init__(self):
        super().__init__()
        self.d[SpendingInterface] = R7WorldAdvisorSpending
