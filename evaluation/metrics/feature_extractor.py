"""Extract fixed opponent-model features from evaluation telemetry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_PRODUCTION_STRUCTURES = {"barracks", "gateway", "spawningpool"}
_TECH_STRUCTURES = {
    "assimilator",
    "barrackstechlab",
    "cyberneticscore",
    "extractor",
    "factory",
    "lair",
    "refinery",
    "roboticsfacility",
    "spire",
    "stargate",
    "starport",
    "twilightcouncil",
}


def extract_features(root: str | Path) -> list[dict[str, Any]]:
    """Extract features from one match directory or a batch output directory."""

    path = Path(root)
    match_dirs = _match_dirs(path)
    return [extract_match_features(match_dir) for match_dir in match_dirs]


def extract_features_from_match_dirs(match_dirs: list[str | Path]) -> list[dict[str, Any]]:
    """Extract features from an explicit current-run match directory list."""

    return [extract_match_features(match_dir) for match_dir in match_dirs]


def extract_match_features(match_dir: str | Path) -> dict[str, Any]:
    match_path = Path(match_dir)
    result = _read_json(match_path / "match_result.json")
    events = _read_events(match_path / "telemetry" / "events.jsonl")
    scouting_events = [
        event.get("payload", {})
        for event in events
        if event.get("event_type") == "scouting_observation"
    ]
    game_state_events = [
        event.get("payload", {}) for event in events if event.get("event_type") == "game_state"
    ]
    predictions = [
        event.get("payload", {})
        for event in events
        if event.get("event_type") == "opponent_prediction"
    ]
    strategy_responses = [
        event.get("payload", {})
        for event in events
        if event.get("event_type") == "strategy_response"
    ]
    strategy_switches = [
        event.get("payload", {})
        for event in events
        if event.get("event_type") == "strategy_switch"
    ]
    interventions = [
        event.get("payload", {})
        for event in events
        if event.get("event_type") == "minimal_behavior_intervention"
    ]
    prediction_payloads = [
        payload.get("prediction", {}) for payload in predictions if payload.get("prediction")
    ]
    opponent_model_mode = result.get("opponent_model_mode") or _first_non_empty(
        payload.get("opponent_model_mode") for payload in predictions
    )
    observation_rush_signal_seen = any(
        bool(payload.get("possible_rush_signal")) for payload in scouting_events
    )
    observation_tech_signal_seen = any(
        bool(payload.get("possible_tech_signal")) for payload in scouting_events
    )
    intervention_mode = _first_non_empty(
        payload.get("intervention_mode") for payload in strategy_responses
    )
    return {
        "match_id": result.get("match_id", match_path.name),
        "match_dir": str(match_path),
        "map_id": result.get("map_id"),
        "opponent_id": result.get("opponent_id"),
        "opponent_race": result.get("opponent_race"),
        "opponent_difficulty": result.get("opponent_difficulty"),
        "bot_config_id": result.get("bot_config_id"),
        "opponent_model_mode": opponent_model_mode,
        "intervention_mode": intervention_mode,
        "match_status": result.get("status"),
        "match_duration": result.get("duration_seconds"),
        "first_enemy_seen_time": _first_value(
            payload.get("first_enemy_seen_time") for payload in scouting_events
        ),
        "first_combat_unit_seen_time": _first_time_with_items(
            scouting_events, "seen_enemy_combat_units"
        ),
        "first_enemy_structure_seen_time": _first_time_with_items(
            scouting_events, "enemy_structures_seen"
        ),
        "first_production_structure_seen_time": _first_structure_time(
            scouting_events, _PRODUCTION_STRUCTURES
        ),
        "first_tech_structure_seen_time": _first_structure_time(
            scouting_events, _TECH_STRUCTURES
        ),
        "observation_rush_signal_seen": observation_rush_signal_seen,
        "observation_tech_signal_seen": observation_tech_signal_seen,
        "possible_rush_signal_seen": observation_rush_signal_seen,
        "possible_tech_signal_seen": observation_tech_signal_seen,
        "prediction_rush_risk_max": _max_numeric(
            payload.get("rush_risk") for payload in prediction_payloads
        ),
        "prediction_tech_risk_max": _max_numeric(
            payload.get("tech_risk") for payload in prediction_payloads
        ),
        "prediction_confidence_max": _max_numeric(
            payload.get("confidence") for payload in prediction_payloads
        ),
        "prediction_signals_non_empty_count": sum(
            1 for payload in prediction_payloads if payload.get("signals")
        ),
        "prediction_recommended_response_tags_count": sum(
            len(payload.get("recommended_response_tags") or [])
            for payload in prediction_payloads
        ),
        "prediction_signal_sample": _first_prediction_with_signals(
            match_path, prediction_payloads
        ),
        "selected_response_tag_count": sum(
            1
            for payload in strategy_responses
            if payload.get("selected_response_tag")
            and payload.get("selected_response_tag") != "none"
        ),
        "strategy_switch_count": len(strategy_switches),
        "defensive_posture_count": _count_response_tag(
            strategy_responses, "defensive_posture"
        ),
        "continue_scouting_count": _count_response_tag(
            strategy_responses, "continue_scouting"
        ),
        "tech_alert_count": _count_response_tag(strategy_responses, "tech_alert"),
        "minimal_behavior_intervention_count": len(interventions),
        "minimal_behavior_active_count": sum(
            1 for payload in interventions if payload.get("outcome") == "active"
        ),
        "minimal_behavior_skipped_count": sum(
            1 for payload in interventions if payload.get("outcome") == "skipped"
        ),
        "visible_enemy_units_max": max(
            (int(payload.get("visible_enemy_units_count", 0)) for payload in game_state_events),
            default=0,
        ),
        "visible_enemy_structures_max": max(
            (
                int(payload.get("visible_enemy_structures_count", 0))
                for payload in game_state_events
            ),
            default=0,
        ),
        "replay_path": result.get("replay_path"),
    }


def _match_dirs(path: Path) -> list[Path]:
    if (path / "match_result.json").exists():
        return [path]
    if not path.exists():
        return []
    return sorted(item.parent for item in path.glob("*/match_result.json"))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
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


def _first_value(values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _first_non_empty(values: Any) -> Any:
    for value in values:
        if value:
            return value
    return None


def _first_time_with_items(events: list[dict[str, Any]], field: str) -> float | None:
    for payload in events:
        if payload.get(field):
            return payload.get("game_time")
    return None


def _first_structure_time(
    events: list[dict[str, Any]], structure_names: set[str]
) -> float | None:
    for payload in events:
        structures = {
            str(item).lower().replace("_", "") for item in payload.get("enemy_structures_seen", [])
        }
        if structures.intersection(structure_names):
            return payload.get("game_time")
    return None


def _max_numeric(values: Any) -> float:
    numeric_values: list[float] = []
    for value in values:
        if value is None:
            continue
        try:
            numeric_values.append(float(value))
        except (TypeError, ValueError):
            continue
    if not numeric_values:
        return 0.0
    return max(numeric_values)


def _first_prediction_with_signals(
    match_path: Path, prediction_payloads: list[dict[str, Any]]
) -> dict[str, Any] | None:
    for payload in prediction_payloads:
        if payload.get("signals"):
            return {
                "match_dir": str(match_path),
                "opening_type": payload.get("opening_type"),
                "rush_risk": payload.get("rush_risk"),
                "tech_risk": payload.get("tech_risk"),
                "confidence": payload.get("confidence"),
                "prediction_mode": payload.get("prediction_mode"),
                "signals": payload.get("signals") or [],
                "recommended_response_tags": payload.get("recommended_response_tags") or [],
            }
    return None


def _count_response_tag(events: list[dict[str, Any]], tag: str) -> int:
    return sum(1 for payload in events if payload.get("selected_response_tag") == tag)
