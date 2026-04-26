"""Module-level runtime state for R7 advisor arms."""

from __future__ import annotations

from pathlib import Path

ACTIVE_ARM = "baseline"
WORLD_MODEL_PATH = ""


def configure(*, arm: str, world_model_path: str = "") -> None:
    global ACTIVE_ARM, WORLD_MODEL_PATH
    ACTIVE_ARM = arm
    WORLD_MODEL_PATH = world_model_path


def world_model_path() -> Path:
    return Path(WORLD_MODEL_PATH).expanduser().resolve()

