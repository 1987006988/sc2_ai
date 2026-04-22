"""YAML config loader for the bot skeleton."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from sc2bot.config.schema import (
    BotConfig,
    BotIdentityConfig,
    BuildOrderConfig,
    ManagersConfig,
    OpponentModelConfig,
    RuntimeConfig,
    TelemetryConfig,
)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in config: {path}")
    return data


def load_bot_config(path: str | Path) -> BotConfig:
    config_path = Path(path)
    data = _read_yaml(config_path)
    bot = data.get("bot", {})
    managers = data.get("managers", {})
    opponent_model = data.get("opponent_model", {})
    runtime = data.get("runtime", {})
    build_order = data.get("build_order", {})
    telemetry = data.get("telemetry", {})
    return BotConfig(
        bot=BotIdentityConfig(
            name=bot.get("name", "sc2-ai"),
            race=bot.get("race", "protoss"),
            strategy=bot.get("strategy", "default"),
        ),
        managers=ManagersConfig(**{k: v for k, v in managers.items() if k in ManagersConfig.__annotations__}),
        opponent_model=OpponentModelConfig(
            **{
                k: v
                for k, v in opponent_model.items()
                if k in OpponentModelConfig.__annotations__ and v is not None
            }
        ),
        runtime=RuntimeConfig(
            **{k: v for k, v in runtime.items() if k in RuntimeConfig.__annotations__}
        ),
        build_order=BuildOrderConfig(
            **{
                k: v
                for k, v in build_order.items()
                if k in BuildOrderConfig.__annotations__ and v is not None
            }
        ),
        telemetry=TelemetryConfig(
            enabled=telemetry.get("enabled", True),
            output_dir=telemetry.get("output_dir", "data/logs/telemetry"),
            verbose=telemetry.get("verbose", False),
        ),
    )
