from evaluation.metrics.schemas import ArtifactCompleteness, DatasetManifest


def test_dataset_manifest_schema_accepts_phase_a_fields():
    manifest = DatasetManifest(
        run_id="phase_a_baseline_v0",
        created_at="2026-04-22T00:00:00+00:00",
        purpose="baseline_v0",
        included_match_dirs=("run/m1", "run/m2"),
        excluded_historical_dirs=("old/m0",),
        map_pool=("incorporeal_aie_v4",),
        opponent_pool=("builtin_easy_terran", "builtin_medium_terran"),
        bot_configs=("default",),
        config_snapshot={"evaluation": {"repeats": 1}},
        match_count=2,
        status_counts={"max_game_time_reached": 1, "completed": 1},
        artifact_completeness=ArtifactCompleteness(
            match_result_count=2,
            replay_count=2,
            telemetry_count=2,
        ),
        evidence_paths=("run/m1", "run/m2", "dataset_manifest.json"),
        chunk_run_ids=("chunk_1",),
        source_manifests=("chunk_1/dataset_manifest.json",),
    )

    assert manifest.validation_errors() == []
    assert manifest.excluded_historical_dirs == ("old/m0",)
    assert manifest.chunk_run_ids == ("chunk_1",)
    assert manifest.artifact_completeness.replay_count == 2


def test_dataset_manifest_schema_flags_count_mismatches():
    manifest = DatasetManifest(
        run_id="run",
        created_at="2026-04-22T00:00:00+00:00",
        purpose="baseline_v0",
        included_match_dirs=("run/m1",),
        excluded_historical_dirs=(),
        map_pool=("map",),
        opponent_pool=("opponent",),
        bot_configs=("default",),
        config_snapshot={},
        match_count=2,
        status_counts={"completed": 1},
        artifact_completeness=ArtifactCompleteness(),
        evidence_paths=("dataset_manifest.json",),
    )

    assert "match_count must equal the number of included_match_dirs" in manifest.validation_errors()
    assert "status_counts must sum to match_count" in manifest.validation_errors()


def test_dataset_manifest_schema_requires_evidence_paths():
    manifest = DatasetManifest(
        run_id="run",
        created_at="2026-04-22T00:00:00+00:00",
        purpose="smoke",
        included_match_dirs=(),
        excluded_historical_dirs=(),
        map_pool=(),
        opponent_pool=(),
        bot_configs=(),
        config_snapshot={},
        match_count=0,
        status_counts={},
        artifact_completeness=ArtifactCompleteness(),
        evidence_paths=(),
    )

    assert "missing evidence_paths" in manifest.validation_errors()
