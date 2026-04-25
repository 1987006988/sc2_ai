from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ARMY_BUCKETS = (
    (0, "none"),
    (1, "low"),
    (9, "medium"),
    (17, "high"),
)


@dataclass(frozen=True)
class HiddenStateLabels:
    opening_class: str
    hidden_tech_path: str
    future_expansion_within_horizon: bool
    hidden_army_bucket: str
    future_contact_risk: bool
    time_to_first_contact: float | None
    next_macro_threat_indicator: str


def _frames(sample: dict[str, Any]) -> list[dict[str, Any]]:
    frames = sample.get("frames", [])
    if not isinstance(frames, list) or not frames:
        raise ValueError("sample.frames must be a non-empty list")
    return frames


def opening_class_from_sample(sample: dict[str, Any]) -> str:
    frames = _frames(sample)
    if "opening_hint" in sample:
        return str(sample["opening_hint"])
    early = [frame for frame in frames if float(frame.get("game_time", 0.0)) <= 120.0]
    gas_seen = max(int(frame.get("enemy_gas_structures", 0)) for frame in early)
    production_seen = max(int(frame.get("enemy_production_structures", 0)) for frame in early)
    if gas_seen >= 2:
        return "gas_opening"
    if production_seen >= 2:
        return "production_opening"
    return "econ_opening"


def hidden_tech_path_from_sample(sample: dict[str, Any]) -> str:
    if "hidden_tech_path" in sample:
        return str(sample["hidden_tech_path"])
    frames = _frames(sample)
    tags = {str(frame.get("enemy_tech_path_hint", "unknown")) for frame in frames}
    tags.discard("unknown")
    if tags:
        return sorted(tags)[0]
    gas_peak = max(int(frame.get("enemy_gas_structures", 0)) for frame in frames)
    return "teching" if gas_peak >= 2 else "ground_unknown"


def future_expansion_within_horizon_from_sample(sample: dict[str, Any], horizon_seconds: float = 120.0) -> bool:
    frames = _frames(sample)
    start_time = float(frames[0].get("game_time", 0.0))
    for frame in frames:
        game_time = float(frame.get("game_time", start_time))
        if game_time - start_time > horizon_seconds:
            break
        if bool(frame.get("enemy_expansion_seen", False)):
            return True
    return False


def hidden_army_bucket_from_sample(sample: dict[str, Any]) -> str:
    if "hidden_army_bucket" in sample:
        return str(sample["hidden_army_bucket"])
    frames = _frames(sample)
    peak_supply = max(int(frame.get("enemy_visible_army_supply", 0)) for frame in frames)
    bucket = "none"
    for threshold, candidate in ARMY_BUCKETS:
        if peak_supply >= threshold:
            bucket = candidate
    return bucket


def future_contact_risk_from_sample(sample: dict[str, Any], threshold: float = 0.6) -> bool:
    frames = _frames(sample)
    return any(float(frame.get("enemy_contact_risk", 0.0)) >= threshold for frame in frames)


def time_to_first_contact_from_sample(sample: dict[str, Any]) -> float | None:
    frames = _frames(sample)
    start_time = float(frames[0].get("game_time", 0.0))
    for frame in frames:
        if bool(frame.get("enemy_contact_seen", False)):
            return float(frame.get("game_time", start_time)) - start_time
    return None


def next_macro_threat_indicator_from_sample(sample: dict[str, Any]) -> str:
    if "next_macro_threat_indicator" in sample:
        return str(sample["next_macro_threat_indicator"])
    if future_contact_risk_from_sample(sample, threshold=0.75):
        return "immediate_pressure"
    if future_expansion_within_horizon_from_sample(sample):
        return "economic_greed"
    tech_path = hidden_tech_path_from_sample(sample)
    if tech_path not in {"ground_unknown", "unknown"}:
        return "tech_transition"
    return "standard_pressure"


def extract_hidden_state_labels(sample: dict[str, Any]) -> HiddenStateLabels:
    return HiddenStateLabels(
        opening_class=opening_class_from_sample(sample),
        hidden_tech_path=hidden_tech_path_from_sample(sample),
        future_expansion_within_horizon=future_expansion_within_horizon_from_sample(sample),
        hidden_army_bucket=hidden_army_bucket_from_sample(sample),
        future_contact_risk=future_contact_risk_from_sample(sample),
        time_to_first_contact=time_to_first_contact_from_sample(sample),
        next_macro_threat_indicator=next_macro_threat_indicator_from_sample(sample),
    )
