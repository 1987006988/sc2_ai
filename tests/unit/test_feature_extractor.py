import json

from evaluation.metrics.feature_extractor import extract_features
from evaluation.metrics.opponent_model_metrics import (
    build_ablation_summary,
    build_strategy_intervention_report,
    write_summary_json,
)


def test_extract_features_handles_complete_match(tmp_path):
    match_dir = tmp_path / "reallaunch-test"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "m1",
                "map_id": "map",
                "opponent_id": "opp",
                "opponent_race": "terran",
                "opponent_difficulty": "easy",
                "bot_config_id": "rule_based",
                "opponent_model_mode": "rule_based",
                "status": "max_game_time_reached",
                "duration_seconds": 12.0,
                "replay_path": "match.SC2Replay",
            }
        ),
        encoding="utf-8",
    )
    events = [
        {
            "event_type": "scouting_observation",
            "payload": {
                "game_time": 10.0,
                "first_enemy_seen_time": 10.0,
                "seen_enemy_combat_units": ["marine"],
                "enemy_structures_seen": ["barracks", "refinery"],
                "possible_rush_signal": True,
                "possible_tech_signal": True,
            },
        },
        {
            "event_type": "opponent_prediction",
            "payload": {
                "opponent_model_mode": "rule_based",
                "prediction": {
                    "rush_risk": 0.7,
                    "tech_risk": 0.2,
                    "confidence": 0.6,
                    "prediction_mode": "prediction_only",
                    "signals": ["early_combat_unit"],
                    "recommended_response_tags": ["prediction_only", "watch_for_rush"],
                },
            },
        },
        {
            "event_type": "game_state",
            "payload": {
                "visible_enemy_units_count": 3,
                "visible_enemy_structures_count": 2,
            },
        },
        {
            "event_type": "strategy_response",
            "payload": {
                "selected_response_tag": "defensive_posture",
                "strategy_switch_reason": "rush_risk_high",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "strategy_switch",
            "payload": {
                "selected_response_tag": "defensive_posture",
                "strategy_switch_reason": "rush_risk_high",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "minimal_behavior_intervention",
            "payload": {
                "action": "army_defense",
                "outcome": "active",
                "reason": "defensive_posture",
                "selected_response_tag": "defensive_posture",
                "intervention_mode": "minimal_behavior",
            },
        },
    ]
    (telemetry_dir / "events.jsonl").write_text(
        "\n".join(json.dumps(event) for event in events), encoding="utf-8"
    )

    features = extract_features(tmp_path)

    assert features[0]["match_id"] == "m1"
    assert features[0]["first_enemy_seen_time"] == 10.0
    assert features[0]["first_combat_unit_seen_time"] == 10.0
    assert features[0]["first_production_structure_seen_time"] == 10.0
    assert features[0]["first_tech_structure_seen_time"] == 10.0
    assert features[0]["observation_rush_signal_seen"] is True
    assert features[0]["observation_tech_signal_seen"] is True
    assert features[0]["prediction_rush_risk_max"] == 0.7
    assert features[0]["prediction_tech_risk_max"] == 0.2
    assert features[0]["prediction_confidence_max"] == 0.6
    assert features[0]["prediction_signals_non_empty_count"] == 1
    assert features[0]["prediction_recommended_response_tags_count"] == 2
    assert features[0]["intervention_mode"] == "minimal_behavior"
    assert features[0]["selected_response_tag_count"] == 1
    assert features[0]["strategy_switch_count"] == 1
    assert features[0]["defensive_posture_count"] == 1
    assert features[0]["continue_scouting_count"] == 0
    assert features[0]["tech_alert_count"] == 0
    assert features[0]["minimal_behavior_intervention_count"] == 1
    assert features[0]["minimal_behavior_active_count"] == 1
    assert features[0]["minimal_behavior_skipped_count"] == 0
    assert features[0]["visible_enemy_units_max"] == 3


def test_extract_features_handles_missing_telemetry(tmp_path):
    match_dir = tmp_path / "reallaunch-test"
    match_dir.mkdir()
    (match_dir / "match_result.json").write_text(
        json.dumps({"match_id": "m1", "status": "launch_error"}), encoding="utf-8"
    )

    features = extract_features(match_dir)

    assert features[0]["match_id"] == "m1"
    assert features[0]["first_enemy_seen_time"] is None
    assert features[0]["visible_enemy_units_max"] == 0


def test_extract_features_returns_all_batch_matches(tmp_path):
    for match_id in ("m1", "m2"):
        match_dir = tmp_path / f"reallaunch-{match_id}"
        telemetry_dir = match_dir / "telemetry"
        telemetry_dir.mkdir(parents=True)
        (match_dir / "match_result.json").write_text(
            json.dumps(
                {
                    "match_id": match_id,
                    "map_id": "map",
                    "opponent_id": "opp",
                    "status": "max_game_time_reached",
                }
            ),
            encoding="utf-8",
        )
        (telemetry_dir / "events.jsonl").write_text("", encoding="utf-8")

    features = extract_features(tmp_path)

    assert [feature["match_id"] for feature in features] == ["m1", "m2"]


def test_extract_features_returns_empty_for_missing_batch_dir(tmp_path):
    features = extract_features(tmp_path / "missing")

    assert features == []


def test_extract_features_reads_phase1e_strategy_response_fields(tmp_path):
    match_dir = tmp_path / "reallaunch-phase1e"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "phase1e",
                "bot_config_id": "minimal_behavior",
                "opponent_model_mode": "rule_based",
                "status": "max_game_time_reached",
            }
        ),
        encoding="utf-8",
    )
    events = [
        {
            "event_type": "strategy_response",
            "payload": {
                "selected_response_tag": "continue_scouting",
                "strategy_switch_reason": "low_information",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "strategy_response",
            "payload": {
                "selected_response_tag": "tech_alert",
                "strategy_switch_reason": "tech_risk_high",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "strategy_switch",
            "payload": {
                "selected_response_tag": "continue_scouting",
                "strategy_switch_reason": "low_information",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "minimal_behavior_intervention",
            "payload": {
                "action": "scout_persistence",
                "outcome": "active",
                "reason": "continue_scouting",
                "selected_response_tag": "continue_scouting",
                "intervention_mode": "minimal_behavior",
            },
        },
        {
            "event_type": "minimal_behavior_intervention",
            "payload": {
                "action": "army_defense",
                "outcome": "skipped",
                "reason": "no_army_available",
                "selected_response_tag": "defensive_posture",
                "intervention_mode": "minimal_behavior",
            },
        },
    ]
    (telemetry_dir / "events.jsonl").write_text(
        "\n".join(json.dumps(event) for event in events), encoding="utf-8"
    )

    features = extract_features(match_dir)

    assert features[0]["intervention_mode"] == "minimal_behavior"
    assert features[0]["selected_response_tag_count"] == 2
    assert features[0]["strategy_switch_count"] == 1
    assert features[0]["continue_scouting_count"] == 1
    assert features[0]["tech_alert_count"] == 1
    assert features[0]["defensive_posture_count"] == 0
    assert features[0]["minimal_behavior_intervention_count"] == 2
    assert features[0]["minimal_behavior_active_count"] == 1
    assert features[0]["minimal_behavior_skipped_count"] == 1


def test_write_summary_json_groups_modes_and_statuses(tmp_path):
    match_dir = tmp_path / "eval" / "reallaunch-null"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "m1",
                "map_id": "map",
                "opponent_id": "opp",
                "bot_config_id": "null",
                "opponent_model_mode": "null",
                "status": "max_game_time_reached",
                "duration_seconds": 1.0,
            }
        ),
        encoding="utf-8",
    )
    (telemetry_dir / "events.jsonl").write_text("", encoding="utf-8")
    match_dir = tmp_path / "eval" / "reallaunch-rule"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "m2",
                "map_id": "map",
                "opponent_id": "opp",
                "bot_config_id": "rule_based",
                "opponent_model_mode": "rule_based",
                "status": "max_game_time_reached",
                "duration_seconds": 2.0,
            }
        ),
        encoding="utf-8",
    )
    (telemetry_dir / "events.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "event_type": "scouting_observation",
                        "payload": {
                            "game_time": 4.0,
                            "first_enemy_seen_time": 4.0,
                            "possible_rush_signal": True,
                            "possible_tech_signal": False,
                        },
                    }
                ),
                json.dumps(
                    {
                        "event_type": "opponent_prediction",
                        "payload": {
                            "opponent_model_mode": "rule_based",
                            "prediction": {
                                "rush_risk": 0.55,
                                "tech_risk": 0.1,
                                "confidence": 0.45,
                                "signals": ["early_combat_unit"],
                                "recommended_response_tags": ["prediction_only"],
                            },
                        },
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    summary = write_summary_json(tmp_path / "eval", tmp_path / "report")

    assert summary["match_count"] == 2
    assert summary["status_counts"] == {"max_game_time_reached": 2}
    assert summary["by_opponent_model_mode"]["null"]["match_count"] == 1
    assert summary["by_opponent_model_mode"]["rule_based"]["match_count"] == 1
    assert summary["by_opponent_model_mode"]["rule_based"]["observation_rush_signal_matches"] == 1
    assert summary["by_opponent_model_mode"]["rule_based"]["prediction_rush_risk_max"] == 0.55
    assert summary["by_opponent_model_mode"]["rule_based"]["prediction_signals_non_empty_count"] == 1
    assert (tmp_path / "report" / "summary.json").exists()
    assert not (tmp_path / "report" / "report.md").exists()


def test_build_ablation_summary_generates_markdown_report(tmp_path):
    match_dir = tmp_path / "eval" / "reallaunch-rule"
    telemetry_dir = match_dir / "telemetry"
    telemetry_dir.mkdir(parents=True)
    (match_dir / "match_result.json").write_text(
        json.dumps(
            {
                "match_id": "m1",
                "map_id": "map",
                "opponent_id": "opp",
                "bot_config_id": "rule_based",
                "opponent_model_mode": "rule_based",
                "status": "max_game_time_reached",
                "duration_seconds": 1.0,
            }
        ),
        encoding="utf-8",
    )
    (telemetry_dir / "events.jsonl").write_text("", encoding="utf-8")

    summary = build_ablation_summary(tmp_path / "eval", tmp_path / "report")
    report = (tmp_path / "report" / "report.md").read_text(encoding="utf-8")

    assert summary["match_count"] == 1
    assert (tmp_path / "report" / "summary.json").exists()
    assert "prediction-only ablation" in report
    assert "Observation-derived signals" in report
    assert "does not prove" in report
    assert "improves win rate" in report


def test_build_ablation_summary_can_use_explicit_match_dirs(tmp_path):
    for match_id in ("old", "current"):
        match_dir = tmp_path / "eval" / f"reallaunch-{match_id}"
        telemetry_dir = match_dir / "telemetry"
        telemetry_dir.mkdir(parents=True)
        (match_dir / "match_result.json").write_text(
            json.dumps(
                {
                    "match_id": match_id,
                    "map_id": "map",
                    "opponent_id": "opp",
                    "bot_config_id": "null",
                    "opponent_model_mode": "null",
                    "status": "max_game_time_reached",
                }
            ),
            encoding="utf-8",
        )
        (telemetry_dir / "events.jsonl").write_text("", encoding="utf-8")

    summary = build_ablation_summary(
        tmp_path / "eval",
        tmp_path / "report",
        run_id="current-run",
        match_dirs=[tmp_path / "eval" / "reallaunch-current"],
    )

    assert summary["run_id"] == "current-run"
    assert summary["output_scope"] == "explicit_match_dirs"
    assert summary["match_count"] == 1
    assert summary["historical_match_count_excluded"] == 1


def test_build_strategy_intervention_report_summarizes_response_tags(tmp_path):
    for bot_config_id, intervention_count in (("null", 0), ("minimal_behavior", 2)):
        match_dir = tmp_path / "eval" / f"reallaunch-{bot_config_id}"
        telemetry_dir = match_dir / "telemetry"
        telemetry_dir.mkdir(parents=True)
        (match_dir / "match_result.json").write_text(
            json.dumps(
                {
                    "match_id": bot_config_id,
                    "map_id": "map",
                    "opponent_id": "opp",
                    "bot_config_id": bot_config_id,
                    "opponent_model_mode": "rule_based" if bot_config_id != "null" else "null",
                    "status": "max_game_time_reached",
                }
            ),
            encoding="utf-8",
        )
        events = [
            {
                "event_type": "strategy_response",
                "payload": {
                    "selected_response_tag": "continue_scouting",
                    "strategy_switch_reason": "low_information",
                    "intervention_mode": "minimal_behavior"
                    if bot_config_id == "minimal_behavior"
                    else "none",
                },
            },
            {
                "event_type": "strategy_switch",
                "payload": {
                    "selected_response_tag": "continue_scouting",
                    "strategy_switch_reason": "low_information",
                    "intervention_mode": "minimal_behavior"
                    if bot_config_id == "minimal_behavior"
                    else "none",
                },
            },
        ]
        for _ in range(intervention_count):
            events.append(
                {
                    "event_type": "minimal_behavior_intervention",
                    "payload": {
                        "action": "scout_persistence",
                        "outcome": "active",
                        "selected_response_tag": "continue_scouting",
                        "intervention_mode": "minimal_behavior",
                    },
                }
            )
        (telemetry_dir / "events.jsonl").write_text(
            "\n".join(json.dumps(event) for event in events),
            encoding="utf-8",
        )

    summary = build_strategy_intervention_report(tmp_path / "eval", tmp_path / "report")
    report = (tmp_path / "report" / "report.md").read_text(encoding="utf-8")

    assert summary["report_type"] == "phase1e_strategy_intervention"
    assert summary["match_count"] == 2
    assert summary["by_bot_config"]["minimal_behavior"][
        "minimal_behavior_intervention_count"
    ] == 2
    assert summary["by_bot_config"]["minimal_behavior"]["selected_response_tag_count"] == 1
    assert "Phase 1E Minimal Strategy Intervention V0" in report
    assert "Response-tag metrics" in report
    assert "does not prove win-rate improvement" in report
    assert "does not prove gameplay quality improvement" in report
