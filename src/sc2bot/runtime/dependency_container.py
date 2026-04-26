"""Dependency construction for managers and services."""

from __future__ import annotations

from dataclasses import dataclass

from sc2bot.config.schema import BotConfig, OpponentModelConfig
from sc2bot.managers.macro_manager import MacroManager
from sc2bot.managers.micro_manager import MicroManager
from sc2bot.managers.scouting_manager import ScoutingManager
from sc2bot.managers.strategy_manager import StrategyManager
from sc2bot.managers.tactical_manager import TacticalManager
from sc2bot.opponent_model.null_model import NullOpponentModel
from sc2bot.opponent_model.r7_rule_macro_model import R7RuleMacroAdvisorOpponentModel
from sc2bot.opponent_model.r7_world_model_model import R7WorldModelOpponentModel
from sc2bot.opponent_model.rule_based_model import RuleBasedOpponentModel
from sc2bot.opponent_model.temporal_runtime_model import TemporalBeliefOpponentModel
from sc2bot.opponent_model.interface import OpponentModel
from sc2bot.telemetry.event_logger import EventLogger


@dataclass
class DependencyContainer:
    telemetry: EventLogger
    macro: MacroManager
    scouting: ScoutingManager
    strategy: StrategyManager
    tactical: TacticalManager
    micro: MicroManager
    opponent_model: OpponentModel
    opponent_model_mode: str = "null"
    opponent_model_config: OpponentModelConfig = OpponentModelConfig()
    runtime_exit_reason: str | None = None

    @classmethod
    def from_config(cls, config: BotConfig) -> "DependencyContainer":
        telemetry = EventLogger(config.telemetry.output_dir, enabled=config.telemetry.enabled)
        opponent_model: OpponentModel
        if config.opponent_model.mode == "rule_based":
            opponent_model = RuleBasedOpponentModel()
        elif config.opponent_model.mode == "rule_based_macro_advisor":
            opponent_model = R7RuleMacroAdvisorOpponentModel()
        elif config.opponent_model.mode == "learned_world_model_advisor":
            opponent_model = R7WorldModelOpponentModel(
                config.opponent_model.model_checkpoint_path,
                history_window=3,
            )
        elif config.opponent_model.mode == "learned_temporal_belief":
            opponent_model = TemporalBeliefOpponentModel(
                config.opponent_model.model_checkpoint_path,
                device=config.opponent_model.model_device,
                history_window=config.opponent_model.temporal_history_window,
            )
        else:
            opponent_model = NullOpponentModel()
        return cls(
            telemetry=telemetry,
            macro=MacroManager(),
            scouting=ScoutingManager(telemetry=telemetry),
            strategy=StrategyManager(),
            tactical=TacticalManager(build_order=config.build_order),
            micro=MicroManager(),
            opponent_model=opponent_model,
            opponent_model_mode=config.opponent_model.mode,
            opponent_model_config=config.opponent_model,
        )
