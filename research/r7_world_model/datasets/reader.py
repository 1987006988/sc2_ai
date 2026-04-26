from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL_KEYS = {
    "sample_id",
    "source_id",
    "replay_id",
    "game_time",
    "map",
    "matchup",
    "own_visible_state",
    "observed_enemy_state",
    "hidden_enemy_label",
    "macro_action_label",
    "candidate_action_slate",
    "future_outcome_label",
    "winner",
    "split",
    "provenance",
    "frames",
}


def validate_sample(sample: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_TOP_LEVEL_KEYS - sample.keys()
    if missing:
        errors.append(f"missing_keys:{sorted(missing)}")
    frames = sample.get("frames")
    if not isinstance(frames, list) or not frames:
        errors.append("frames_must_be_non_empty_list")
        return errors
    for idx, frame in enumerate(frames):
        if "game_time" not in frame:
            errors.append(f"frame_{idx}_missing_game_time")
    return errors


def load_jsonl_samples(path: Path) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            samples.append(json.loads(line))
    return samples


def load_and_validate_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    samples = load_jsonl_samples(path)
    errors: list[str] = []
    for idx, sample in enumerate(samples):
        sample_errors = validate_sample(sample)
        errors.extend(f"sample_{idx}:{err}" for err in sample_errors)
    return samples, errors
