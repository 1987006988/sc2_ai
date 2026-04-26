from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from research.r7_world_model.parsers.di_star_replay_parser import parse_replay_to_samples


def _split_for_replay(replay_name: str) -> str:
    score = sum(ord(ch) for ch in replay_name)
    bucket = score % 10
    if bucket <= 5:
        return "train"
    if bucket <= 7:
        return "val"
    return "test"


def _write_jsonl(path: Path, samples: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for sample in samples:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize the R7 teacher replay dataset from DI-star replays.")
    parser.add_argument("--replay-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    replay_paths = sorted(args.replay_dir.glob("*.SC2Replay"))
    if not replay_paths:
        raise ValueError(f"no replays found in {args.replay_dir}")

    split_rows: dict[str, list[dict[str, Any]]] = {"train": [], "val": [], "test": []}
    replay_assignments: dict[str, str] = {}

    for replay_path in replay_paths:
        parsed_samples = parse_replay_to_samples(replay_path)
        split = _split_for_replay(replay_path.name)
        replay_assignments[replay_path.name] = split
        for parsed in parsed_samples:
            row = dict(parsed.sample)
            row["split"] = split
            split_rows[split].append(row)

    if not all(split_rows.values()):
        raise ValueError("train/val/test must all be non-empty")

    for split_name, rows in split_rows.items():
        _write_jsonl(args.output_dir / f"{split_name}.jsonl", rows)

    label_summary = {
        "enemy_opening_class": dict(Counter(row["enemy_opening_class"] for rows in split_rows.values() for row in rows)),
        "enemy_tech_path": dict(Counter(row["enemy_tech_path"] for rows in split_rows.values() for row in rows)),
        "macro_action_label": dict(Counter(row["macro_action_label"] for rows in split_rows.values() for row in rows)),
        "production_tempo_label": dict(
            Counter(row["production_tempo_label"] for rows in split_rows.values() for row in rows)
        ),
        "future_winner": dict(Counter(row["future_winner"] for rows in split_rows.values() for row in rows)),
        "future_game_length_bucket": dict(
            Counter(row["future_game_length_bucket"] for rows in split_rows.values() for row in rows)
        ),
        "future_pressure_proxy": dict(
            Counter(row["future_pressure_proxy"] for rows in split_rows.values() for row in rows)
        ),
    }
    manifest = {
        "dataset_id": "r7_teacher_dataset_v0_proxy",
        "status": "valid",
        "source_id": "distar_zvz_agent_platform",
        "replay_dir": str(args.replay_dir),
        "replay_count": len(replay_paths),
        "split_counts": {split: len(rows) for split, rows in split_rows.items()},
        "replay_assignments": replay_assignments,
        "label_summary": label_summary,
        "claim_boundary": "teacher_proxy_dataset_derived_from_command_events_not_full_counterfactual_ground_truth",
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R7_TEACHER_DATASET_VALID")
    print(f"replays={len(replay_paths)}")
    print(f"train={len(split_rows['train'])} val={len(split_rows['val'])} test={len(split_rows['test'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
