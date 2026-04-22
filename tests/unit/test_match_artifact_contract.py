from evaluation.metrics.schemas import MatchArtifactContract


def test_match_artifact_contract_maps_existing_match_result_payload():
    payload = {
        "match_id": "reallaunch-abc123",
        "status": "max_game_time_reached",
        "result": "Result.Defeat",
        "mode": "real_launch",
        "bot_config": "configs/bot/default.yaml",
        "bot_config_id": "default",
        "opponent_model_mode": "null",
        "map_id": "incorporeal_aie_v4",
        "opponent_id": "builtin_easy_terran",
        "opponent_race": "terran",
        "opponent_difficulty": "easy",
        "telemetry_path": "telemetry/events.jsonl",
        "replay_path": "match.SC2Replay",
        "failure_reason": None,
        "started_at": "2026-04-22T00:00:00+00:00",
        "completed_at": "2026-04-22T00:01:00+00:00",
        "duration_seconds": 60.0,
    }

    contract = MatchArtifactContract.from_match_result_payload(
        payload,
        match_result_path="run/reallaunch-abc123/match_result.json",
        run_id="phase_a_probe",
    )

    assert contract.run_id == "phase_a_probe"
    assert contract.match_id == "reallaunch-abc123"
    assert contract.map_id == "incorporeal_aie_v4"
    assert contract.opponent_id == "builtin_easy_terran"
    assert contract.opponent_race == "terran"
    assert contract.opponent_difficulty == "easy"
    assert contract.bot_config_id == "default"
    assert contract.start_time == "2026-04-22T00:00:00+00:00"
    assert contract.end_time == "2026-04-22T00:01:00+00:00"
    assert contract.status == "max_game_time_reached"
    assert contract.failure_reason is None
    assert contract.replay_path == "match.SC2Replay"
    assert contract.telemetry_path == "telemetry/events.jsonl"
    assert contract.match_result_path == "run/reallaunch-abc123/match_result.json"
    assert contract.config_reference == "configs/bot/default.yaml"
    assert contract.sc2_version is None
    assert contract.git_commit is None
    assert contract.metadata["mode"] == "real_launch"
    assert contract.validation_errors() == []


def test_match_artifact_contract_flags_missing_required_fields():
    contract = MatchArtifactContract.from_match_result_payload(
        {"match_id": "m1", "status": "launch_error"},
        match_result_path="run/m1/match_result.json",
    )

    assert contract.run_id == "m1"
    assert "missing required field: map_id" in contract.validation_errors()
    assert "missing required field: opponent_id" in contract.validation_errors()
    assert "missing required field: bot_config_id" in contract.validation_errors()
    assert "missing config_reference or config_snapshot" in contract.validation_errors()


def test_match_artifact_contract_accepts_config_snapshot_instead_of_reference():
    contract = MatchArtifactContract(
        run_id="run",
        match_id="match",
        map_id="map",
        opponent_id="opponent",
        opponent_race=None,
        opponent_difficulty=None,
        bot_config_id="bot",
        start_time=None,
        end_time=None,
        status="completed",
        failure_reason=None,
        replay_path=None,
        telemetry_path=None,
        match_result_path="match_result.json",
        config_snapshot={"bot": {"race": "Protoss"}},
    )

    assert contract.validation_errors() == []
