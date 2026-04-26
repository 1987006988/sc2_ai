from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from research.r7_world_model.parsers.di_star_replay_parser import parse_replay_to_samples


REPLAY_PATH = Path("third_party/strong_bots/DI-star/data/replays/replay_4.10.0.SC2Replay")


def test_parse_replay_to_samples_emits_required_labels() -> None:
    samples = parse_replay_to_samples(REPLAY_PATH)
    assert samples
    sample = samples[0].sample
    assert sample["enemy_opening_class"]
    assert sample["enemy_tech_path"]
    assert sample["macro_action_label"]
    assert sample["future_winner"] in {"win", "loss"}
    assert sample["future_game_length_bucket"] in {"short", "medium", "long"}


def test_materializer_and_benchmark_run(tmp_path: Path) -> None:
    replay_dir = REPLAY_PATH.parent
    dataset_dir = tmp_path / "dataset"
    manifest_path = tmp_path / "manifest.json"
    benchmark_path = tmp_path / "benchmark.json"

    subprocess.run(
        [
            sys.executable,
            "research/r7_world_model/datasets/materialize_teacher_dataset.py",
            "--replay-dir",
            str(replay_dir),
            "--output-dir",
            str(dataset_dir),
            "--manifest",
            str(manifest_path),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            "research/r7_world_model/eval/run_teacher_benchmark.py",
            "--train",
            str(dataset_dir / "train.jsonl"),
            "--val",
            str(dataset_dir / "val.jsonl"),
            "--test",
            str(dataset_dir / "test.jsonl"),
            "--output",
            str(benchmark_path),
        ],
        check=True,
    )
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    assert benchmark["status"] == "valid"
    assert benchmark["splits"]["test"]["leaderboard"]
