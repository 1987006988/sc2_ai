import json

from evaluation.metrics.failure_accounting import build_failure_accounting_summary


def _write_match(match_dir, *, status, replay=True, telemetry=True, duration=10.0):
    match_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": match_dir.name,
                "status": status,
                "duration_seconds": duration,
            }
        ),
        encoding="utf-8",
    )
    if replay:
        (match_dir / "match.SC2Replay").write_text("replay", encoding="utf-8")
    if telemetry:
        telemetry_dir = match_dir / "telemetry"
        telemetry_dir.mkdir()
        (telemetry_dir / "events.jsonl").write_text("{}", encoding="utf-8")


def test_failure_accounting_counts_statuses_and_artifacts(tmp_path):
    _write_match(tmp_path / "reallaunch-a", status="completed")
    _write_match(tmp_path / "reallaunch-b", status="max_game_time_reached", replay=False)
    _write_match(tmp_path / "reallaunch-c", status="launch_error", telemetry=False)

    summary = build_failure_accounting_summary(tmp_path, run_id="smoke")

    assert summary["run_id"] == "smoke"
    assert summary["total_matches"] == 3
    assert summary["completed_count"] == 1
    assert summary["max_game_time_reached_count"] == 1
    assert summary["crashed_count"] == 1
    assert summary["timeout_count"] == 0
    assert summary["missing_replay_count"] == 1
    assert summary["missing_telemetry_count"] == 1
    assert summary["missing_match_result_count"] == 0
    assert summary["crash_rate"] == 1 / 3
    assert summary["timeout_rate"] == 0.0
    assert summary["artifact_completeness_rate"] == 7 / 9


def test_failure_accounting_handles_empty_root(tmp_path):
    summary = build_failure_accounting_summary(tmp_path)

    assert summary["total_matches"] == 0
    assert summary["crash_rate"] == 0.0
    assert summary["timeout_rate"] == 0.0
    assert summary["artifact_completeness_rate"] == 0.0
