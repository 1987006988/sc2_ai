from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from research.r6_temporal_belief.datasets.reader import load_and_validate_jsonl
from research.r6_temporal_belief.eval.metrics import evaluate_prediction_bundle
from research.r6_temporal_belief.eval.offline_baselines import (
    build_static_prior,
    label_dict,
    rule_based_predictor,
    shallow_temporal_predictor,
    static_prior_predictor,
)


def _load_split(path: Path) -> list[dict[str, Any]]:
    samples, errors = load_and_validate_jsonl(path)
    if errors:
        raise ValueError(f"invalid split {path}: {errors}")
    return samples


def _mean_balanced_accuracy(report: dict[str, dict[str, float]]) -> float:
    if not report:
        return 0.0
    return sum(metrics["balanced_accuracy"] for metrics in report.values()) / len(report)


def _evaluate_split(name: str, samples: list[dict[str, Any]], priors: dict[str, Any]) -> dict[str, Any]:
    truths = [label_dict(sample) for sample in samples]
    comparator_predictions = {
        "rule_based": [rule_based_predictor(sample) for sample in samples],
        "static_prior": [static_prior_predictor(priors, sample) for sample in samples],
        "shallow_temporal": [shallow_temporal_predictor(sample) for sample in samples],
    }
    comparator_reports = {
        comparator: evaluate_prediction_bundle(truths, predictions)
        for comparator, predictions in comparator_predictions.items()
    }
    leaderboard = sorted(
        (
            {
                "comparator": comparator,
                "mean_balanced_accuracy": round(_mean_balanced_accuracy(report), 6),
            }
            for comparator, report in comparator_reports.items()
        ),
        key=lambda row: row["mean_balanced_accuracy"],
        reverse=True,
    )
    return {
        "split_name": name,
        "sample_count": len(samples),
        "leaderboard": leaderboard,
        "comparators": comparator_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the R6 offline baseline benchmark.")
    parser.add_argument("--train", required=True, type=Path)
    parser.add_argument("--val", required=True, type=Path)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    train_samples = _load_split(args.train)
    val_samples = _load_split(args.val)
    test_samples = _load_split(args.test)
    if not train_samples or not val_samples or not test_samples:
        raise ValueError("train/val/test must all be non-empty for a valid offline benchmark")

    priors = build_static_prior(train_samples)
    results = {
        "benchmark_id": "r6_offline_hidden_state_benchmark_v0",
        "status": "valid",
        "train_sample_count": len(train_samples),
        "val_sample_count": len(val_samples),
        "test_sample_count": len(test_samples),
        "train_static_priors": priors,
        "splits": {
            "val": _evaluate_split("val", val_samples, priors),
            "test": _evaluate_split("test", test_samples, priors),
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R6_OFFLINE_BENCHMARK_VALID")
    print(f"output={args.output}")
    print(f"train={len(train_samples)} val={len(val_samples)} test={len(test_samples)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
