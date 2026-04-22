import json

from evaluation.reports.run_phase_a_a1_report import build_phase_a_a1_report


def test_phase_a_a1_report_labels_smoke_as_infrastructure_only(tmp_path):
    probe_dir = tmp_path / "probe"
    smoke_dir = tmp_path / "smoke"
    output_dir = tmp_path / "report"
    probe_dir.mkdir()
    smoke_dir.mkdir()
    (probe_dir / "dataset_manifest.json").write_text(
        json.dumps(
            {
                "match_count": 1,
                "status_counts": {"max_game_time_reached": 1},
                "evidence_paths": ["probe/match_result.json"],
            }
        ),
        encoding="utf-8",
    )
    (smoke_dir / "dataset_manifest.json").write_text(
        json.dumps({"match_count": 4, "evidence_paths": ["smoke/match_result.json"]}),
        encoding="utf-8",
    )
    (smoke_dir / "failure_accounting_summary.json").write_text(
        json.dumps(
            {
                "total_matches": 4,
                "status_counts": {"max_game_time_reached": 4},
                "crash_rate": 0.0,
                "timeout_rate": 0.0,
                "artifact_completeness_rate": 1.0,
                "missing_replay_count": 0,
                "missing_telemetry_count": 0,
                "evidence_paths": ["smoke/replay.SC2Replay"],
            }
        ),
        encoding="utf-8",
    )

    summary = build_phase_a_a1_report(
        probe_dir=probe_dir,
        smoke_dir=smoke_dir,
        output_dir=output_dir,
        run_id="a1",
    )

    assert summary["run_id"] == "a1"
    assert summary["probe"]["match_count"] == 1
    assert summary["smoke"]["total_matches"] == 4
    assert "one probe plus four smoke matches are not a baseline dataset" in summary["limitations"]
    assert (output_dir / "summary.json").exists()
    report = (output_dir / "report.md").read_text(encoding="utf-8")
    assert "infrastructure evidence only" in report
    assert "do not constitute a baseline dataset" in report
