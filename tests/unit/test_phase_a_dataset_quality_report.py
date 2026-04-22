import json

from evaluation.reports.run_phase_a_dataset_quality_report import (
    build_phase_a_dataset_quality_report,
)


def test_phase_a_dataset_quality_report_uses_manifest_match_dirs(tmp_path):
    match_dir = tmp_path / "run" / "match_1"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match.SC2Replay").write_bytes(b"replay")
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "match_1",
                "status": "max_game_time_reached",
                "map_id": "map_a",
                "opponent_id": "opponent_a",
                "opponent_race": "terran",
                "opponent_difficulty": "easy",
                "bot_config_id": "default",
                "duration_seconds": 12.5,
            }
        ),
        encoding="utf-8",
    )
    (telemetry_dir / "events.jsonl").write_text(
        "\n".join(
            [
                json.dumps({"event_type": "match_started", "payload": {}}),
                json.dumps({"event_type": "sc2_match_started", "payload": {}}),
                json.dumps(
                    {
                        "event_type": "scouting_observation",
                        "payload": {"first_enemy_seen_time": 4.0},
                    }
                ),
                json.dumps({"event_type": "game_state", "payload": {}}),
                json.dumps({"event_type": "opponent_prediction", "payload": {}}),
                json.dumps({"event_type": "strategy_response", "payload": {}}),
                json.dumps({"event_type": "worker_scout_dispatched", "payload": {}}),
                json.dumps({"event_type": "sc2_match_exit_requested", "payload": {}}),
            ]
        ),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "dataset_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "run_id": "phase_a_baseline_v0",
                "included_match_dirs": [str(match_dir)],
                "map_pool": ["map_a"],
                "opponent_pool": ["opponent_a"],
                "bot_configs": ["default"],
                "status_counts": {"max_game_time_reached": 1},
                "artifact_completeness": {
                    "match_result_count": 1,
                    "replay_count": 1,
                    "telemetry_count": 1,
                    "missing_match_result_count": 0,
                    "missing_replay_count": 0,
                    "missing_telemetry_count": 0,
                },
                "source_manifests": ["chunk_1.json"],
                "excluded_historical_dirs": [],
            }
        ),
        encoding="utf-8",
    )

    summary = build_phase_a_dataset_quality_report(
        manifest_path=manifest_path,
        output_dir=tmp_path / "report",
    )

    assert summary["match_count"] == 1
    assert summary["replay_availability"] == 1.0
    assert summary["telemetry_availability"] == 1.0
    assert summary["opponent_races"] == {"terran": 1}
    assert summary["match_duration_seconds"]["avg"] == 12.5
    assert summary["first_enemy_seen_time_seconds"]["min"] == 4.0
    assert summary["first_scout_time_seconds"]["reason"]
    assert summary["scout_dispatch_event_count"] == 1
    assert summary["telemetry_event_coverage"]["game_state"]["matches_with_event"] == 1
    report = (tmp_path / "report" / "report.md").read_text(encoding="utf-8")
    assert "It measures dataset and artifact quality, not bot strength." in report
