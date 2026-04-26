from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from research.r7_world_model.datasets.reader import load_and_validate_jsonl
from research.r7_world_model.eval.baselines import (
    TASK_GROUPS,
    TASKS,
    build_rule_tables,
    build_shallow_temporal_index,
    build_static_prior,
    rule_based_predictor,
    shallow_temporal_predictor,
    static_prior_predictor,
)
from research.r7_world_model.eval.metrics import evaluate_predictions


def _load_split(path: Path) -> list[dict[str, Any]]:
    samples, errors = load_and_validate_jsonl(path)
    if errors:
        raise ValueError(f"invalid split {path}: {errors}")
    return samples


def _evaluate_split(
    samples: list[dict[str, Any]],
    global_priors: dict[str, Any],
    rule_tables: dict[str, dict[str, Any]],
    shallow_index: list[dict[str, Any]],
) -> dict[str, Any]:
    truths = {task: [sample[task] for sample in samples] for task in TASKS}
    comparator_predictions = {
        "static_prior": [{task: static_prior_predictor(global_priors, sample)[task] for task in TASKS} for sample in samples],
        "rule_based": [{task: rule_based_predictor(sample, global_priors, rule_tables)[task] for task in TASKS} for sample in samples],
        "shallow_temporal": [{task: shallow_temporal_predictor(sample, shallow_index)[task] for task in TASKS} for sample in samples],
    }
    comparator_reports: dict[str, Any] = {}
    for comparator, rows in comparator_predictions.items():
        task_metrics = {
            task: evaluate_predictions(truths[task], [row[task] for row in rows])
            for task in TASKS
        }
        grouped_scores = {
            group_name: round(
                sum(task_metrics[task]["balanced_accuracy"] for task in group_tasks) / len(group_tasks),
                6,
            )
            for group_name, group_tasks in TASK_GROUPS.items()
        }
        comparator_reports[comparator] = {
            "tasks": task_metrics,
            "group_balanced_accuracy": grouped_scores,
            "aggregate_balanced_accuracy": round(
                sum(grouped_scores.values()) / len(grouped_scores),
                6,
            ),
        }
    leaderboard = sorted(
        (
            {
                "comparator": comparator,
                "aggregate_balanced_accuracy": report["aggregate_balanced_accuracy"],
            }
            for comparator, report in comparator_reports.items()
        ),
        key=lambda row: row["aggregate_balanced_accuracy"],
        reverse=True,
    )
    return {"leaderboard": leaderboard, "comparators": comparator_reports, "sample_count": len(samples)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the R7 teacher benchmark.")
    parser.add_argument("--train", required=True, type=Path)
    parser.add_argument("--val", required=True, type=Path)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    train_samples = _load_split(args.train)
    val_samples = _load_split(args.val)
    test_samples = _load_split(args.test)
    if not train_samples or not val_samples or not test_samples:
        raise ValueError("train/val/test must all be non-empty")

    global_priors = build_static_prior(train_samples)
    rule_tables = build_rule_tables(train_samples, global_priors)
    shallow_index = build_shallow_temporal_index(train_samples)
    results = {
        "benchmark_id": "r7_teacher_benchmark_v0_proxy",
        "status": "valid",
        "claim_boundary": "teacher_proxy_benchmark_from_replay_command_sequences",
        "train_sample_count": len(train_samples),
        "val_sample_count": len(val_samples),
        "test_sample_count": len(test_samples),
        "global_priors": global_priors,
        "splits": {
            "val": _evaluate_split(val_samples, global_priors, rule_tables, shallow_index),
            "test": _evaluate_split(test_samples, global_priors, rule_tables, shallow_index),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R7_TEACHER_BENCHMARK_VALID")
    print(f"output={args.output}")
    print(f"train={len(train_samples)} val={len(val_samples)} test={len(test_samples)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
