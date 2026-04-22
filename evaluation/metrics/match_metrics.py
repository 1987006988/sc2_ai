"""Basic match metric helpers."""

from evaluation.metrics.schemas import MatchMetrics


def crash_rate(metrics: list[MatchMetrics]) -> float:
    if not metrics:
        return 0.0
    return sum(1 for item in metrics if item.crashed) / len(metrics)
