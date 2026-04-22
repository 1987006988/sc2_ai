"""Build the Phase A Baseline Dataset V0 quality report from real match data."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


CRASH_STATUSES = {"gameplay_error", "launch_error", "config_error"}
TIMEOUT_STATUSES = {"timeout"}
CORE_TELEMETRY_EVENTS = (
    "match_started",
    "sc2_match_started",
    "game_state",
    "scouting_observation",
    "opponent_prediction",
    "strategy_response",
    "sc2_match_exit_requested",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def _summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "max": None, "avg": None}
    return {"min": min(values), "max": max(values), "avg": mean(values)}


def _first_value(values: list[float | None]) -> float | None:
    for value in values:
        if value is not None:
            return value
    return None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_report(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Phase A Baseline Dataset V0 Quality Report",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Evidence type: `{summary['evidence_type']}`",
        f"- Data source: `{summary['data_source']}`",
        f"- Match count: `{summary['match_count']}`",
        f"- Maps: `{summary['maps']}`",
        f"- Opponent races: `{summary['opponent_races']}`",
        f"- Opponent difficulties: `{summary['opponent_difficulties']}`",
        f"- Status counts: `{summary['status_counts']}`",
        f"- Crash rate: `{summary['crash_rate']}`",
        f"- Timeout rate: `{summary['timeout_rate']}`",
        f"- Replay availability: `{summary['replay_availability']}`",
        f"- Telemetry availability: `{summary['telemetry_availability']}`",
        "",
        "## Artifact Completeness",
        "",
        f"- Match results: `{summary['artifact_completeness']['match_result_count']}`",
        f"- Replays: `{summary['artifact_completeness']['replay_count']}`",
        f"- Telemetry files: `{summary['artifact_completeness']['telemetry_count']}`",
        f"- Missing replays: `{summary['artifact_completeness']['missing_replay_count']}`",
        f"- Missing telemetry: `{summary['artifact_completeness']['missing_telemetry_count']}`",
        "",
        "## Match Duration",
        "",
        f"- Duration seconds: `{summary['match_duration_seconds']}`",
        "",
        "## Telemetry Event Coverage",
        "",
    ]
    for event_type, coverage in summary["telemetry_event_coverage"].items():
        lines.append(f"- `{event_type}`: `{coverage}`")
    lines.extend(
        [
            "",
            "## Scout Timing",
            "",
            f"- First enemy seen time seconds: `{summary['first_enemy_seen_time_seconds']}`",
            f"- First scout dispatch time seconds: `{summary['first_scout_time_seconds']}`",
            f"- Scout dispatch event count: `{summary['scout_dispatch_event_count']}`",
            "",
            "## Current Bot Behavior Limitations",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in summary["current_bot_behavior_limitations"])
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This report uses real Phase A baseline match outputs.",
            "- It measures dataset and artifact quality, not bot strength.",
            "- It does not prove ladder competitiveness, win-rate quality, or gameplay improvement.",
            "- Synthetic and dry-run evidence are not used for capability claims in this report.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_phase_a_dataset_quality_report(
    *,
    manifest_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    manifest = _read_json(manifest_path)
    match_dirs = [Path(path) for path in manifest.get("included_match_dirs", [])]

    status_counts: Counter[str] = Counter()
    opponent_races: Counter[str] = Counter()
    opponent_difficulties: Counter[str] = Counter()
    opponent_ids: Counter[str] = Counter()
    durations: list[float] = []
    first_enemy_seen_times: list[float] = []
    event_counts: Counter[str] = Counter()
    matches_with_event: Counter[str] = Counter()
    scout_dispatch_event_count = 0

    missing_replay_count = 0
    missing_telemetry_count = 0
    missing_match_result_count = 0

    for match_dir in match_dirs:
        match_result_path = match_dir / "match_result.json"
        replay_path = match_dir / "match.SC2Replay"
        telemetry_path = match_dir / "telemetry" / "events.jsonl"

        if not match_result_path.exists():
            missing_match_result_count += 1
            continue
        result = _read_json(match_result_path)
        status_counts[str(result.get("status") or "unknown")] += 1
        opponent_races[str(result.get("opponent_race") or "unknown")] += 1
        opponent_difficulties[str(result.get("opponent_difficulty") or "unknown")] += 1
        opponent_ids[str(result.get("opponent_id") or "unknown")] += 1
        duration = result.get("duration_seconds")
        if isinstance(duration, int | float):
            durations.append(float(duration))

        if not replay_path.exists():
            missing_replay_count += 1
        if not telemetry_path.exists():
            missing_telemetry_count += 1
            continue

        events = _read_events(telemetry_path)
        event_types_in_match = {str(event.get("event_type")) for event in events}
        for event_type in event_types_in_match:
            matches_with_event[event_type] += 1
        for event in events:
            event_type = str(event.get("event_type"))
            event_counts[event_type] += 1
            payload = event.get("payload", {})
            if event_type == "scouting_observation":
                first_enemy_seen = payload.get("first_enemy_seen_time")
                if isinstance(first_enemy_seen, int | float):
                    first_enemy_seen_times.append(float(first_enemy_seen))
            if event_type == "worker_scout_dispatched":
                scout_dispatch_event_count += 1

    total_matches = len(match_dirs)
    crashed_count = sum(status_counts.get(status, 0) for status in CRASH_STATUSES)
    timeout_count = sum(status_counts.get(status, 0) for status in TIMEOUT_STATUSES)
    telemetry_event_coverage = {
        event_type: {
            "matches_with_event": matches_with_event.get(event_type, 0),
            "match_coverage_rate": (
                matches_with_event.get(event_type, 0) / total_matches
                if total_matches
                else 0.0
            ),
            "event_count": event_counts.get(event_type, 0),
        }
        for event_type in CORE_TELEMETRY_EVENTS
    }
    observed_non_core_events = sorted(
        event_type
        for event_type in event_counts
        if event_type not in CORE_TELEMETRY_EVENTS
    )

    artifact_completeness = manifest.get("artifact_completeness", {})
    summary = {
        "run_id": manifest.get("run_id"),
        "evidence_type": "real_match_baseline_dataset",
        "data_source": str(manifest_path),
        "output_scope": "merged_phase_a_baseline_v0_manifest_only",
        "historical_match_count_excluded": None,
        "match_count": total_matches,
        "maps": manifest.get("map_pool", []),
        "opponents": dict(sorted(opponent_ids.items())),
        "opponent_races": dict(sorted(opponent_races.items())),
        "opponent_difficulties": dict(sorted(opponent_difficulties.items())),
        "bot_configs": manifest.get("bot_configs", []),
        "status_counts": dict(status_counts),
        "crash_rate": crashed_count / total_matches if total_matches else 0.0,
        "timeout_rate": timeout_count / total_matches if total_matches else 0.0,
        "artifact_completeness": {
            **artifact_completeness,
            "missing_match_result_count_observed": missing_match_result_count,
            "missing_replay_count_observed": missing_replay_count,
            "missing_telemetry_count_observed": missing_telemetry_count,
        },
        "replay_availability": (
            (total_matches - missing_replay_count) / total_matches
            if total_matches
            else 0.0
        ),
        "telemetry_availability": (
            (total_matches - missing_telemetry_count) / total_matches
            if total_matches
            else 0.0
        ),
        "match_duration_seconds": _summary(durations),
        "first_enemy_seen_time_seconds": _summary(first_enemy_seen_times),
        "first_scout_time_seconds": {
            "min": None,
            "max": None,
            "avg": None,
            "reason": "worker_scout_dispatched telemetry currently has no game_time field",
        },
        "scout_dispatch_event_count": scout_dispatch_event_count,
        "telemetry_event_coverage": telemetry_event_coverage,
        "observed_non_core_event_types": observed_non_core_events,
        "source_manifests": manifest.get("source_manifests", []),
        "included_match_dirs": manifest.get("included_match_dirs", []),
        "excluded_historical_dirs": manifest.get("excluded_historical_dirs", []),
        "evidence_paths": [
            str(manifest_path),
            *manifest.get("source_manifests", []),
        ],
        "current_bot_behavior_limitations": [
            "Baseline dataset is collected from the current survival/opponent-model scaffold, not a playable competitive core.",
            "All 24 matches ended with max_game_time_reached, so this dataset does not measure wins or losses as a strength claim.",
            "Current telemetry has scout dispatch events but no game_time on those events, so first_scout_time is unknown.",
            "Combat and build progression quality are not established by this report.",
            "This report does not prove bot strength, ladder competitiveness, or gameplay improvement.",
        ],
    }
    _write_json(output_dir / "summary.json", summary)
    _write_report(output_dir / "report.md", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Phase A baseline dataset quality report."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    summary = build_phase_a_dataset_quality_report(
        manifest_path=Path(args.manifest),
        output_dir=Path(args.output_dir),
    )
    print(
        "phase-a dataset quality report generated: "
        f"{args.output_dir} ({summary['match_count']} matches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
