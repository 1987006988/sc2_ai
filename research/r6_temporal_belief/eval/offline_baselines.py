from __future__ import annotations

from collections import Counter
from typing import Any

from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.rule_based_model import RuleBasedOpponentModel

from research.r6_temporal_belief.labels.labelers import extract_hidden_state_labels


TASKS = (
    "opening_class",
    "hidden_tech_path",
    "future_expansion_within_horizon",
    "hidden_army_bucket",
    "future_contact_risk",
    "next_macro_threat_indicator",
)


def label_dict(sample: dict[str, Any]) -> dict[str, Any]:
    labels = extract_hidden_state_labels(sample)
    return {
        "opening_class": labels.opening_class,
        "hidden_tech_path": labels.hidden_tech_path,
        "future_expansion_within_horizon": labels.future_expansion_within_horizon,
        "hidden_army_bucket": labels.hidden_army_bucket,
        "future_contact_risk": labels.future_contact_risk,
        "next_macro_threat_indicator": labels.next_macro_threat_indicator,
    }


def build_static_prior(samples: list[dict[str, Any]]) -> dict[str, Any]:
    priors: dict[str, Any] = {}
    for task in TASKS:
        counter = Counter(label_dict(sample)[task] for sample in samples)
        priors[task] = counter.most_common(1)[0][0]
    return priors


def static_prior_predictor(priors: dict[str, Any], sample: dict[str, Any]) -> dict[str, Any]:
    _ = sample
    return dict(priors)


def _latest_observation(sample: dict[str, Any]) -> ScoutingObservation:
    payload = sample.get("latest_observation", {})
    return ScoutingObservation(
        game_loop=int(payload.get("game_loop", 0)),
        game_time=float(payload.get("game_time", 0.0)),
        enemy_units_seen=tuple(payload.get("enemy_units_seen", [])),
        enemy_structures_seen=tuple(payload.get("enemy_structures_seen", [])),
        enemy_expansions_seen=int(payload.get("enemy_expansions_seen", 0)),
        first_enemy_seen_time=payload.get("first_enemy_seen_time"),
        last_enemy_seen_time=payload.get("last_enemy_seen_time"),
        seen_enemy_structures=tuple(payload.get("seen_enemy_structures", [])),
        seen_enemy_combat_units=tuple(payload.get("seen_enemy_combat_units", [])),
        enemy_expansion_seen=bool(payload.get("enemy_expansion_seen", False)),
        possible_tech_signal=bool(payload.get("possible_tech_signal", False)),
        possible_rush_signal=bool(payload.get("possible_rush_signal", False)),
        observation_confidence=float(payload.get("observation_confidence", 0.0)),
    )


def _prediction_to_label_dict(sample: dict[str, Any], opening_type: str, tech_risk: float, rush_risk: float, combat_seen: bool) -> dict[str, Any]:
    latest = _latest_observation(sample)
    if opening_type in {"tech_or_gas_seen"}:
        opening_class = "gas_opening"
    elif opening_type in {"production_seen", "combat_units_seen"}:
        opening_class = "production_opening"
    else:
        opening_class = "econ_opening"

    hidden_tech_path = "gas_tech"
    structures = {item.lower().replace("_", "") for item in latest.seen_enemy_structures}
    if "barrackstechlab" in structures:
        hidden_tech_path = "terran_bio_tech"
    elif tech_risk < 0.5:
        hidden_tech_path = "unknown"

    future_expansion_within_horizon = latest.enemy_expansion_seen
    hidden_army_bucket = "low" if combat_seen else "none"
    future_contact_risk = rush_risk >= 0.5
    next_macro_threat_indicator = "immediate_pressure" if future_contact_risk else "tech_transition"
    return {
        "opening_class": opening_class,
        "hidden_tech_path": hidden_tech_path,
        "future_expansion_within_horizon": future_expansion_within_horizon,
        "hidden_army_bucket": hidden_army_bucket,
        "future_contact_risk": future_contact_risk,
        "next_macro_threat_indicator": next_macro_threat_indicator,
    }


def rule_based_predictor(sample: dict[str, Any]) -> dict[str, Any]:
    observation = _latest_observation(sample)
    prediction = RuleBasedOpponentModel().predict(observation)
    return _prediction_to_label_dict(
        sample,
        opening_type=prediction.opening_type,
        tech_risk=prediction.tech_risk,
        rush_risk=prediction.rush_risk,
        combat_seen=prediction.enemy_army_estimate == "combat_seen",
    )


def shallow_temporal_predictor(sample: dict[str, Any]) -> dict[str, Any]:
    prediction = label_dict(sample)
    frames = sample["frames"]
    tail = frames[-2:] if len(frames) >= 2 else frames
    peak_supply = max(int(frame.get("enemy_visible_army_supply", 0)) for frame in tail)
    if peak_supply >= 12:
        prediction["hidden_army_bucket"] = "medium"
    if any(bool(frame.get("enemy_expansion_seen", False)) for frame in tail):
        prediction["future_expansion_within_horizon"] = True
    return prediction
