from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


TASK_GROUPS = {
    "hidden_state": ("enemy_opening_class", "enemy_tech_path"),
    "macro_action": ("macro_action_label", "production_tempo_label"),
    "future_proxy": ("future_winner", "future_game_length_bucket", "future_pressure_proxy"),
}
TASKS = tuple(task for tasks in TASK_GROUPS.values() for task in tasks)


def label_dict(sample: dict[str, Any]) -> dict[str, Any]:
    return {task: sample[task] for task in TASKS}


def _feature_vector(sample: dict[str, Any]) -> list[float]:
    own = sample["own_visible_state"]
    race = own["own_race"]
    enemy_race = sample["observed_enemy_state"]["enemy_race"]
    frames = sample["frames"]
    vector = [
        float(own["expand_count"]),
        float(own["production_count"]),
        float(own["tech_count"]),
        float(own["upgrade_count"]),
        float(own["defense_count"]),
        float(own["combat_unit_count"]),
        float(own["worker_econ_count"]),
        float(own["attack_count"]),
    ]
    for frame in frames:
        vector.extend(
            float(frame[key])
            for key in (
                "expand_count",
                "production_count",
                "tech_count",
                "upgrade_count",
                "defense_count",
                "combat_unit_count",
                "worker_econ_count",
                "attack_count",
            )
        )
    races = ("Protoss", "Terran", "Zerg", "Random")
    vector.extend(1.0 if race == value else 0.0 for value in races)
    vector.extend(1.0 if enemy_race == value else 0.0 for value in races)
    return vector


def build_static_prior(samples: list[dict[str, Any]]) -> dict[str, Any]:
    priors: dict[str, Any] = {}
    for task in TASKS:
        counter = Counter(sample[task] for sample in samples)
        priors[task] = counter.most_common(1)[0][0]
    return priors


def static_prior_predictor(priors: dict[str, Any], sample: dict[str, Any]) -> dict[str, Any]:
    _ = sample
    return dict(priors)


def build_rule_tables(samples: list[dict[str, Any]], global_priors: dict[str, Any]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Counter[Any]]] = defaultdict(lambda: defaultdict(Counter))
    for sample in samples:
        enemy_race = sample["observed_enemy_state"]["enemy_race"]
        own_race = sample["own_visible_state"]["own_race"]
        key = f"{own_race}|{enemy_race}"
        for task in TASKS:
            grouped[key][task][sample[task]] += 1
    tables: dict[str, dict[str, Any]] = {}
    for key, task_counters in grouped.items():
        tables[key] = {
            task: counter.most_common(1)[0][0] if counter else global_priors[task]
            for task, counter in task_counters.items()
        }
    return tables


def rule_based_predictor(sample: dict[str, Any], global_priors: dict[str, Any], rule_tables: dict[str, dict[str, Any]]) -> dict[str, Any]:
    key = f"{sample['own_visible_state']['own_race']}|{sample['observed_enemy_state']['enemy_race']}"
    return dict(rule_tables.get(key, global_priors))


def build_shallow_temporal_index(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"vector": _feature_vector(sample), "labels": label_dict(sample)} for sample in samples]


def _l1_distance(left: list[float], right: list[float]) -> float:
    return sum(abs(a - b) for a, b in zip(left, right))


def shallow_temporal_predictor(sample: dict[str, Any], training_index: list[dict[str, Any]]) -> dict[str, Any]:
    vector = _feature_vector(sample)
    best = min(training_index, key=lambda row: _l1_distance(vector, row["vector"]))
    return dict(best["labels"])
