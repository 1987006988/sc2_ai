"""Typed configuration objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BotIdentityConfig:
    name: str
    race: str
    strategy: str


@dataclass(frozen=True)
class ManagersConfig:
    macro: bool = True
    scouting: bool = True
    strategy: bool = True
    tactical: bool = True
    micro: bool = True


@dataclass(frozen=True)
class OpponentModelConfig:
    mode: str = "null"
    intervention_mode: str = "none"
    rush_risk_threshold: float = 0.5
    tech_risk_threshold: float = 0.5
    low_information_confidence_threshold: float = 0.25
    low_information_game_time_threshold: float = 90.0


@dataclass(frozen=True)
class RuntimeConfig:
    max_game_loop: int = 2600
    max_steps: int | None = None
    worker_production: bool = True
    worker_gather: bool = True
    worker_scout: bool = True
    supply_sustain: bool = True
    supply_sustain_threshold: int = 2
    supply_structure_name: str = "pylon"
    army_defense: bool = True


@dataclass(frozen=True)
class BuildOrderConfig:
    target_probe_count: int = 22
    pylon_supply_buffer: int = 2
    gateway_min_probe_count: int = 16
    gateway_min_game_time: float = 90.0
    assimilator_enabled: bool = True
    cybernetics_core_enabled: bool = True
    zealot_production_priority: int = 10
    stalker_production_priority: int = 20
    attack_army_supply_threshold: int = 8
    attack_game_time_threshold: float = 360.0
    defend_radius: float = 30.0


@dataclass(frozen=True)
class TelemetryConfig:
    enabled: bool = True
    output_dir: str = "data/logs/telemetry"
    verbose: bool = False


@dataclass(frozen=True)
class BotConfig:
    bot: BotIdentityConfig
    managers: ManagersConfig
    opponent_model: OpponentModelConfig
    runtime: RuntimeConfig
    build_order: BuildOrderConfig
    telemetry: TelemetryConfig
