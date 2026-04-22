"""Failure and artifact accounting for real-match output directories."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


CRASH_STATUSES = {"gameplay_error", "launch_error", "config_error"}
TIMEOUT_STATUSES = {"timeout"}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _match_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.parent for path in root.glob("*/match_result.json"))


def build_failure_accounting_summary(root: Path, *, run_id: str | None = None) -> dict[str, Any]:
    match_dirs = _match_dirs(root)
    status_counts: Counter[str] = Counter()
    evidence_paths: list[str] = []
    missing_replay_dirs: list[str] = []
    missing_telemetry_dirs: list[str] = []
    missing_match_result_dirs: list[str] = []
    duration_seconds: list[float] = []

    for match_dir in match_dirs:
        match_result_path = match_dir / "match_result.json"
        replay_path = match_dir / "match.SC2Replay"
        telemetry_path = match_dir / "telemetry" / "events.jsonl"

        if not match_result_path.exists():
            missing_match_result_dirs.append(str(match_dir))
            continue

        payload = _read_json(match_result_path)
        status = str(payload.get("status") or "unknown")
        status_counts[status] += 1
        evidence_paths.append(str(match_result_path))

        if replay_path.exists():
            evidence_paths.append(str(replay_path))
        else:
            missing_replay_dirs.append(str(match_dir))

        if telemetry_path.exists():
            evidence_paths.append(str(telemetry_path))
        else:
            missing_telemetry_dirs.append(str(match_dir))

        duration = payload.get("duration_seconds")
        if isinstance(duration, int | float):
            duration_seconds.append(float(duration))

    total_matches = len(match_dirs)
    completed_count = status_counts.get("completed", 0)
    crashed_count = sum(status_counts.get(status, 0) for status in CRASH_STATUSES)
    timeout_count = sum(status_counts.get(status, 0) for status in TIMEOUT_STATUSES)
    max_game_time_reached_count = status_counts.get("max_game_time_reached", 0)
    expected_artifacts = total_matches * 3
    present_artifacts = (
        (total_matches - len(missing_match_result_dirs))
        + (total_matches - len(missing_replay_dirs))
        + (total_matches - len(missing_telemetry_dirs))
    )

    return {
        "run_id": run_id or root.name,
        "evidence_type": "real_match_smoke",
        "source_root": str(root),
        "total_matches": total_matches,
        "completed_count": completed_count,
        "crashed_count": crashed_count,
        "timeout_count": timeout_count,
        "max_game_time_reached_count": max_game_time_reached_count,
        "status_counts": dict(status_counts),
        "missing_match_result_count": len(missing_match_result_dirs),
        "missing_replay_count": len(missing_replay_dirs),
        "missing_telemetry_count": len(missing_telemetry_dirs),
        "crash_rate": crashed_count / total_matches if total_matches else 0.0,
        "timeout_rate": timeout_count / total_matches if total_matches else 0.0,
        "artifact_completeness_rate": (
            present_artifacts / expected_artifacts if expected_artifacts else 0.0
        ),
        "duration_seconds_min": min(duration_seconds) if duration_seconds else None,
        "duration_seconds_max": max(duration_seconds) if duration_seconds else None,
        "duration_seconds_avg": (
            sum(duration_seconds) / len(duration_seconds) if duration_seconds else None
        ),
        "missing_match_result_dirs": missing_match_result_dirs,
        "missing_replay_dirs": missing_replay_dirs,
        "missing_telemetry_dirs": missing_telemetry_dirs,
        "evidence_paths": tuple(evidence_paths),
        "notes": (
            "real 4-match smoke only",
            "not a baseline dataset",
            "does not prove bot strength",
        ),
    }


def write_failure_accounting_summary(summary: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build failure/artifact accounting summary.")
    parser.add_argument("--input-dir", required=True, help="Real match output root.")
    parser.add_argument("--output", required=True, help="Summary JSON path.")
    parser.add_argument("--run-id", default=None, help="Optional run id override.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    summary = build_failure_accounting_summary(Path(args.input_dir), run_id=args.run_id)
    write_failure_accounting_summary(summary, Path(args.output))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
