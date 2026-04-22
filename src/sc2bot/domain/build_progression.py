"""Phase B build progression and combat capability contract."""

from __future__ import annotations

from dataclasses import dataclass, field


PROBE_PRODUCTION = "probe_production"
PYLON = "pylon"
GATEWAY = "gateway"
ASSIMILATOR = "assimilator"
CYBERNETICS_CORE = "cybernetics_core"
ZEALOT = "zealot"
STALKER = "stalker"
ARMY_RALLY = "army_rally"
ATTACK_ORDER = "attack_order"
DEFEND_ORDER = "defend_order"
COMBAT_EVENT = "combat_event"

REQUIRED_PHASE_B_FEATURES: tuple[str, ...] = (
    PROBE_PRODUCTION,
    PYLON,
    GATEWAY,
    ASSIMILATOR,
    CYBERNETICS_CORE,
    ZEALOT,
    STALKER,
    ARMY_RALLY,
    ATTACK_ORDER,
    DEFEND_ORDER,
    COMBAT_EVENT,
)


@dataclass(frozen=True)
class BuildProgressionContract:
    """Static contract for Phase B gameplay evidence and telemetry coverage."""

    required_features: tuple[str, ...] = REQUIRED_PHASE_B_FEATURES
    build_features: tuple[str, ...] = (
        PROBE_PRODUCTION,
        PYLON,
        GATEWAY,
        ASSIMILATOR,
        CYBERNETICS_CORE,
    )
    combat_unit_features: tuple[str, ...] = (ZEALOT, STALKER)
    army_order_features: tuple[str, ...] = (ARMY_RALLY, ATTACK_ORDER, DEFEND_ORDER)
    telemetry_features: tuple[str, ...] = (COMBAT_EVENT,)
    validation_level_required: str = "L3"
    notes: tuple[str, ...] = field(
        default_factory=lambda: (
            "Unit tests validate this contract only.",
            "Real SC2 probes are required before gameplay behavior is validated.",
        )
    )

    def missing_required_features(self) -> tuple[str, ...]:
        present = {
            *self.build_features,
            *self.combat_unit_features,
            *self.army_order_features,
            *self.telemetry_features,
        }
        return tuple(feature for feature in self.required_features if feature not in present)

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        missing = self.missing_required_features()
        if missing:
            errors.append(f"missing required features: {', '.join(missing)}")
        if len(set(self.required_features)) != len(self.required_features):
            errors.append("required_features contains duplicates")
        if self.validation_level_required != "L3":
            errors.append("Phase B gameplay contract must require L3 real-match validation")
        return errors

    def to_dict(self) -> dict[str, object]:
        return {
            "required_features": list(self.required_features),
            "build_features": list(self.build_features),
            "combat_unit_features": list(self.combat_unit_features),
            "army_order_features": list(self.army_order_features),
            "telemetry_features": list(self.telemetry_features),
            "validation_level_required": self.validation_level_required,
            "notes": list(self.notes),
        }
