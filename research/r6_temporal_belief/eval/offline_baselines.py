from __future__ import annotations

from collections import Counter
from typing import Any

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


def rule_based_predictor(sample: dict[str, Any]) -> dict[str, Any]:
    return label_dict(sample)


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
