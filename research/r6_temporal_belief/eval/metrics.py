from __future__ import annotations

from collections import defaultdict
from typing import Any


def accuracy_score(y_true: list[Any], y_pred: list[Any]) -> float:
    if not y_true:
        return 0.0
    matches = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return matches / len(y_true)


def balanced_accuracy_score(y_true: list[Any], y_pred: list[Any]) -> float:
    if not y_true:
        return 0.0
    by_class: dict[Any, list[int]] = defaultdict(list)
    for true, pred in zip(y_true, y_pred):
        by_class[true].append(1 if true == pred else 0)
    per_class = [sum(values) / len(values) for values in by_class.values()]
    return sum(per_class) / len(per_class)


def evaluate_prediction_bundle(y_true: list[dict[str, Any]], y_pred: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    if not y_true:
        return {}
    keys = y_true[0].keys()
    report: dict[str, dict[str, float]] = {}
    for key in keys:
        true_values = [row[key] for row in y_true]
        pred_values = [row[key] for row in y_pred]
        report[key] = {
            "accuracy": accuracy_score(true_values, pred_values),
            "balanced_accuracy": balanced_accuracy_score(true_values, pred_values),
        }
    return report
