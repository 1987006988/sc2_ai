import pytest

from evaluation.metrics.dataset_manifest import merge_dataset_manifests


def test_merge_dataset_manifests_combines_chunk_fields(tmp_path):
    first = tmp_path / "chunk_1.json"
    second = tmp_path / "chunk_2.json"
    first.write_text(
        """
{
  "run_id": "chunk_1",
  "created_at": "2026-04-22T00:00:00+00:00",
  "purpose": "chunk",
  "included_match_dirs": ["run/m1"],
  "excluded_historical_dirs": [],
  "map_pool": ["map_a"],
  "opponent_pool": ["opponent_a"],
  "bot_configs": ["default"],
  "config_snapshot": {},
  "match_count": 1,
  "status_counts": {"max_game_time_reached": 1},
  "artifact_completeness": {
    "match_result_count": 1,
    "replay_count": 1,
    "telemetry_count": 1,
    "missing_match_result_count": 0,
    "missing_replay_count": 0,
    "missing_telemetry_count": 0
  },
  "evidence_paths": ["run/m1/match_result.json"]
}
""",
        encoding="utf-8",
    )
    second.write_text(
        """
{
  "run_id": "chunk_2",
  "created_at": "2026-04-22T00:00:00+00:00",
  "purpose": "chunk",
  "included_match_dirs": ["run/m2"],
  "excluded_historical_dirs": [],
  "map_pool": ["map_b"],
  "opponent_pool": ["opponent_b"],
  "bot_configs": ["default"],
  "config_snapshot": {},
  "match_count": 1,
  "status_counts": {"completed": 1},
  "artifact_completeness": {
    "match_result_count": 1,
    "replay_count": 0,
    "telemetry_count": 1,
    "missing_match_result_count": 0,
    "missing_replay_count": 1,
    "missing_telemetry_count": 0
  },
  "evidence_paths": ["run/m2/match_result.json"]
}
""",
        encoding="utf-8",
    )

    manifest = merge_dataset_manifests(
        [first, second],
        run_id="merged",
        purpose="test merge",
        excluded_historical_dirs=("old/run",),
        min_match_count=2,
    )

    assert manifest.validation_errors() == []
    assert manifest.match_count == 2
    assert manifest.map_pool == ("map_a", "map_b")
    assert manifest.opponent_pool == ("opponent_a", "opponent_b")
    assert manifest.status_counts == {"max_game_time_reached": 1, "completed": 1}
    assert manifest.artifact_completeness.replay_count == 1
    assert manifest.artifact_completeness.missing_replay_count == 1
    assert manifest.chunk_run_ids == ("chunk_1", "chunk_2")
    assert manifest.excluded_historical_dirs == ("old/run",)


def test_merge_dataset_manifests_blocks_duplicate_match_dirs(tmp_path):
    first = tmp_path / "chunk_1.json"
    second = tmp_path / "chunk_2.json"
    payload = """
{
  "run_id": "chunk",
  "created_at": "2026-04-22T00:00:00+00:00",
  "purpose": "chunk",
  "included_match_dirs": ["run/m1"],
  "excluded_historical_dirs": [],
  "map_pool": ["map"],
  "opponent_pool": ["opponent"],
  "bot_configs": ["default"],
  "config_snapshot": {},
  "match_count": 1,
  "status_counts": {"completed": 1},
  "artifact_completeness": {
    "match_result_count": 1,
    "replay_count": 1,
    "telemetry_count": 1,
    "missing_match_result_count": 0,
    "missing_replay_count": 0,
    "missing_telemetry_count": 0
  },
  "evidence_paths": ["run/m1/match_result.json"]
}
"""
    first.write_text(payload, encoding="utf-8")
    second.write_text(payload, encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate included match dirs"):
        merge_dataset_manifests(
            [first, second],
            run_id="merged",
            purpose="test merge",
        )


def test_merge_dataset_manifests_enforces_minimum_count(tmp_path):
    source = tmp_path / "chunk.json"
    source.write_text(
        """
{
  "run_id": "chunk",
  "created_at": "2026-04-22T00:00:00+00:00",
  "purpose": "chunk",
  "included_match_dirs": ["run/m1"],
  "excluded_historical_dirs": [],
  "map_pool": ["map"],
  "opponent_pool": ["opponent"],
  "bot_configs": ["default"],
  "config_snapshot": {},
  "match_count": 1,
  "status_counts": {"completed": 1},
  "artifact_completeness": {
    "match_result_count": 1,
    "replay_count": 1,
    "telemetry_count": 1,
    "missing_match_result_count": 0,
    "missing_replay_count": 0,
    "missing_telemetry_count": 0
  },
  "evidence_paths": ["run/m1/match_result.json"]
}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="below required minimum"):
        merge_dataset_manifests(
            [source],
            run_id="merged",
            purpose="test merge",
            min_match_count=2,
        )
