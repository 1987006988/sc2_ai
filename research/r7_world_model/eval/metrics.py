from __future__ import annotations

from typing import Any


def _unique_labels(truths: list[Any], predictions: list[Any]) -> list[Any]:
    return sorted({*truths, *predictions}, key=str)


def accuracy(truths: list[Any], predictions: list[Any]) -> float:
    if not truths:
        return 0.0
    correct = sum(1 for truth, pred in zip(truths, predictions) if truth == pred)
    return correct / len(truths)


def balanced_accuracy(truths: list[Any], predictions: list[Any]) -> float:
    labels = _unique_labels(truths, predictions)
    if not labels:
        return 0.0
    recalls: list[float] = []
    for label in labels:
        positives = [idx for idx, truth in enumerate(truths) if truth == label]
        if not positives:
            continue
        true_positive = sum(1 for idx in positives if predictions[idx] == label)
        recalls.append(true_positive / len(positives))
    return sum(recalls) / len(recalls) if recalls else 0.0


def macro_f1(truths: list[Any], predictions: list[Any]) -> float:
    labels = _unique_labels(truths, predictions)
    if not labels:
        return 0.0
    f1s: list[float] = []
    for label in labels:
        tp = sum(1 for truth, pred in zip(truths, predictions) if truth == label and pred == label)
        fp = sum(1 for truth, pred in zip(truths, predictions) if truth != label and pred == label)
        fn = sum(1 for truth, pred in zip(truths, predictions) if truth == label and pred != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        if precision + recall == 0:
            f1s.append(0.0)
        else:
            f1s.append((2 * precision * recall) / (precision + recall))
    return sum(f1s) / len(f1s)


def evaluate_predictions(truths: list[Any], predictions: list[Any]) -> dict[str, float]:
    return {
        "accuracy": round(accuracy(truths, predictions), 6),
        "balanced_accuracy": round(balanced_accuracy(truths, predictions), 6),
        "macro_f1": round(macro_f1(truths, predictions), 6),
    }
