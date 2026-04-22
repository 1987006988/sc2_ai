"""Top-level application object for the bot skeleton."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sc2bot.config.loader import load_bot_config
from sc2bot.config.schema import BotConfig
from sc2bot.runtime.dependency_container import DependencyContainer
from sc2bot.runtime.game_loop import GameLoop


@dataclass
class BotApp:
    """Small composition root for runtime dependencies."""

    config: BotConfig
    container: DependencyContainer

    @classmethod
    def from_config(cls, config_path: Path) -> "BotApp":
        config = load_bot_config(config_path)
        return cls.from_bot_config(config)

    @classmethod
    def from_bot_config(cls, config: BotConfig) -> "BotApp":
        container = DependencyContainer.from_config(config)
        return cls(config=config, container=container)

    def initialize(self) -> None:
        self.container.telemetry.record(
            "match_started",
            {
                "bot": self.config.bot.name,
                "opponent_model_mode": self.config.opponent_model.mode,
            },
        )

    def run(self) -> None:
        """Run one skeleton game-loop tick.

        Real SC2 runtime integration is intentionally deferred until the framework
        choice is verified.
        """

        loop = GameLoop(self.container)
        loop.step()
