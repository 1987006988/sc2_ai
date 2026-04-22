"""Opponent-model ablation metrics and report generation."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.metrics.feature_extractor import extract_features, extract_features_from_match_dirs


def prediction_accuracy(correct: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return correct / total


def build_ablation_summary(
    evaluation_dir: str | Path,
    report_output_dir: str | Path,
    *,
    run_id: str | None = None,
    match_dirs: list[str | Path] | None = None,
) -> dict[str, Any]:
    summary = build_metrics_summary(evaluation_dir, run_id=run_id, match_dirs=match_dirs)
    output_dir = Path(report_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "report.md").write_text(render_markdown_report(summary), encoding="utf-8")
    return summary


def build_strategy_intervention_report(
    evaluation_dir: str | Path,
    report_output_dir: str | Path,
    *,
    run_id: str | None = None,
    match_dirs: list[str | Path] | None = None,
) -> dict[str, Any]:
    summary = build_strategy_intervention_summary(
        evaluation_dir, run_id=run_id, match_dirs=match_dirs
    )
    output_dir = Path(report_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "report.md").write_text(
        render_strategy_intervention_report(summary), encoding="utf-8"
    )
    return summary


def build_strategy_intervention_summary(
    evaluation_dir: str | Path,
    *,
    run_id: str | None = None,
    match_dirs: list[str | Path] | None = None,
) -> dict[str, Any]:
    base = build_metrics_summary(evaluation_dir, run_id=run_id, match_dirs=match_dirs)
    features = base["features"]
    return {
        **base,
        "report_type": "phase1e_strategy_intervention",
        "by_bot_config": _group_by_bot_config(features),
        "prediction_timeline_summary": _prediction_timeline_summary(features),
        "known_limitations": [
            "This is a minimal intervention telemetry ablation.",
            "The intervention is intentionally thin and config-gated.",
            "This report does not prove win-rate improvement.",
            "This report does not prove gameplay quality improvement.",
            "Response tags and intervention counts show that code paths executed, not that decisions are strategically optimal.",
        ],
        "next_experiment_recommendation": (
            "Review response-tag and intervention telemetry before deciding whether any "
            "minimal behavior should be retained for a demo freeze."
        ),
    }


def build_metrics_summary(
    evaluation_dir: str | Path,
    *,
    run_id: str | None = None,
    match_dirs: list[str | Path] | None = None,
) -> dict[str, Any]:
    """Build the machine-readable opponent-model ablation summary payload."""

    if match_dirs is None:
        features = extract_features(evaluation_dir)
        selected_match_dirs = [item.get("match_dir") for item in features if item.get("match_dir")]
        historical_match_count_excluded = 0
        historical_match_dirs: list[str] = []
        output_scope = "evaluation_dir"
    else:
        features = extract_features_from_match_dirs(match_dirs)
        selected_match_dirs = [str(Path(match_dir)) for match_dir in match_dirs]
        selected = {str(Path(match_dir)) for match_dir in match_dirs}
        all_features = extract_features(evaluation_dir)
        historical_match_dirs = [
            str(item.get("match_dir"))
            for item in all_features
            if item.get("match_dir") and str(Path(item["match_dir"])) not in selected
        ]
        historical_match_count_excluded = len(historical_match_dirs)
        output_scope = "explicit_match_dirs"
    return {
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id or Path(evaluation_dir).name,
        "evaluation_dir": str(evaluation_dir),
        "output_scope": output_scope,
        "selected_match_dirs": selected_match_dirs,
        "historical_match_count_excluded": historical_match_count_excluded,
        "historical_match_dirs": historical_match_dirs,
        "match_count": len(features),
        "map_list": sorted({item.get("map_id") for item in features if item.get("map_id")}),
        "opponent_list": sorted(
            {item.get("opponent_id") for item in features if item.get("opponent_id")}
        ),
        "bot_config_list": sorted(
            {item.get("bot_config_id") for item in features if item.get("bot_config_id")}
        ),
        "status_counts": dict(Counter(item.get("match_status") for item in features)),
        "by_opponent_model_mode": _group_by_mode(features),
        "rule_based_non_empty_prediction_signal_sample": _rule_based_signal_sample(features),
        "features": features,
        "known_limitations": [
            "This is a prediction-only ablation.",
            "The rule-based model does not change gameplay behavior.",
            "This report does not prove win-rate improvement.",
            "Observation-derived signals come from scouting telemetry and are not opponent-model predictions.",
        ],
        "next_experiment_recommendation": (
            "Use the extracted risk signals to design a small behavior intervention, "
            "then rerun the same fixed pool."
        ),
    }


def write_summary_json(
    evaluation_dir: str | Path,
    output_dir: str | Path,
    *,
    run_id: str | None = None,
    match_dirs: list[str | Path] | None = None,
) -> dict[str, Any]:
    """Write only summary.json, without rendering a markdown report."""

    summary = build_metrics_summary(evaluation_dir, run_id=run_id, match_dirs=match_dirs)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def render_markdown_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 1D Opponent Model Ablation V0",
        "",
        f"- Run timestamp: `{summary['run_timestamp']}`",
        f"- Run id: `{summary['run_id']}`",
        f"- Evaluation dir: `{summary['evaluation_dir']}`",
        f"- Output scope: `{summary['output_scope']}`",
        f"- Match count: `{summary['match_count']}`",
        f"- Maps: {', '.join(summary['map_list']) or 'none'}",
        f"- Opponents: {', '.join(summary['opponent_list']) or 'none'}",
        f"- Bot configs: {', '.join(summary['bot_config_list']) or 'none'}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"- `{status}`: {count}")
    if summary.get("historical_match_count_excluded"):
        lines.extend(
            [
                "",
                "## Historical Results Excluded",
                "",
                (
                    "- Historical match directories excluded from this summary: "
                    f"`{summary['historical_match_count_excluded']}`"
                ),
            ]
        )
    lines.extend(["", "## Opponent Model Mode Comparison", ""])
    for mode, payload in sorted(summary["by_opponent_model_mode"].items()):
        lines.extend(
            [
                f"### {mode}",
                "",
                f"- Matches: `{payload['match_count']}`",
                f"- First enemy seen average: `{payload['first_enemy_seen_time_avg']}`",
                f"- Observation rush signal matches: `{payload['observation_rush_signal_matches']}`",
                f"- Observation tech signal matches: `{payload['observation_tech_signal_matches']}`",
                f"- Prediction rush risk max: `{payload['prediction_rush_risk_max']}`",
                f"- Prediction tech risk max: `{payload['prediction_tech_risk_max']}`",
                f"- Prediction confidence max: `{payload['prediction_confidence_max']}`",
                (
                    "- Prediction non-empty signal events: "
                    f"`{payload['prediction_signals_non_empty_count']}`"
                ),
                (
                    "- Prediction recommended response tag count: "
                    f"`{payload['prediction_recommended_response_tags_count']}`"
                ),
                f"- Max visible enemy units: `{payload['visible_enemy_units_max']}`",
                f"- Max visible enemy structures: `{payload['visible_enemy_structures_max']}`",
                "",
            ]
        )
    sample = summary.get("rule_based_non_empty_prediction_signal_sample")
    lines.extend(["## Rule-Based Prediction Signal Sample", ""])
    if sample:
        lines.extend(
            [
                f"- Match dir: `{sample['match_dir']}`",
                f"- Opening type: `{sample.get('opening_type')}`",
                f"- Rush risk: `{sample.get('rush_risk')}`",
                f"- Tech risk: `{sample.get('tech_risk')}`",
                f"- Confidence: `{sample.get('confidence')}`",
                f"- Prediction mode: `{sample.get('prediction_mode')}`",
                f"- Signals: `{', '.join(sample.get('signals') or []) or 'none'}`",
                (
                    "- Recommended response tags: "
                    f"`{', '.join(sample.get('recommended_response_tags') or []) or 'none'}`"
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                (
                    "No real rule_based `opponent_prediction` event with non-empty signals "
                    "was found in this report input."
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation",
            "",
            "This is a prediction-only ablation. It validates configuration switching, "
            "prediction telemetry, feature extraction, and reporting. It does not prove "
            "that the rule-based opponent model improves win rate or gameplay quality.",
            "",
            "Observation-derived signals are raw scouting telemetry signals. Prediction-derived "
            "signals come only from `opponent_prediction` events. Observation signals should not "
            "be treated as opponent-model prediction quality.",
            "",
            "## Known Limitations",
            "",
        ]
    )
    for item in summary["known_limitations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Experiment", "", summary["next_experiment_recommendation"], ""])
    return "\n".join(lines)


def render_strategy_intervention_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Phase 1E Minimal Strategy Intervention V0",
        "",
        f"- Run timestamp: `{summary['run_timestamp']}`",
        f"- Run id: `{summary['run_id']}`",
        f"- Evaluation dir: `{summary['evaluation_dir']}`",
        f"- Output scope: `{summary['output_scope']}`",
        f"- Match count: `{summary['match_count']}`",
        f"- Maps: {', '.join(summary['map_list']) or 'none'}",
        f"- Opponents: {', '.join(summary['opponent_list']) or 'none'}",
        f"- Bot configs: {', '.join(summary['bot_config_list']) or 'none'}",
        "",
        "## Status Counts",
        "",
    ]
    for status, count in sorted(summary["status_counts"].items()):
        lines.append(f"- `{status}`: {count}")

    lines.extend(["", "## Bot Config Comparison", ""])
    for bot_config_id, payload in sorted(summary["by_bot_config"].items()):
        lines.extend(
            [
                f"### {bot_config_id}",
                "",
                f"- Matches: `{payload['match_count']}`",
                f"- Status counts: `{payload['status_counts']}`",
                f"- Opponent model modes: `{', '.join(payload['opponent_model_modes']) or 'none'}`",
                f"- Intervention modes: `{', '.join(payload['intervention_modes']) or 'none'}`",
                f"- Prediction rush risk max: `{payload['prediction_rush_risk_max']}`",
                f"- Prediction tech risk max: `{payload['prediction_tech_risk_max']}`",
                f"- Prediction confidence max: `{payload['prediction_confidence_max']}`",
                f"- Selected response tag count: `{payload['selected_response_tag_count']}`",
                f"- Strategy switch count: `{payload['strategy_switch_count']}`",
                f"- Defensive posture count: `{payload['defensive_posture_count']}`",
                f"- Continue scouting count: `{payload['continue_scouting_count']}`",
                f"- Tech alert count: `{payload['tech_alert_count']}`",
                f"- Minimal behavior intervention count: `{payload['minimal_behavior_intervention_count']}`",
                f"- Minimal behavior active count: `{payload['minimal_behavior_active_count']}`",
                f"- Minimal behavior skipped count: `{payload['minimal_behavior_skipped_count']}`",
                "",
            ]
        )

    lines.extend(["## Prediction Timeline Summary", ""])
    for item in summary["prediction_timeline_summary"]:
        lines.append(
            "- "
            f"`{item['match_id']}` / `{item['bot_config_id']}` / `{item['opponent_id']}`: "
            f"first_enemy_seen={item['first_enemy_seen_time']}, "
            f"rush_max={item['prediction_rush_risk_max']}, "
            f"tech_max={item['prediction_tech_risk_max']}, "
            f"selected_tags={item['selected_response_tag_count']}, "
            f"switches={item['strategy_switch_count']}, "
            f"interventions={item['minimal_behavior_intervention_count']}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This is a minimal strategy-intervention telemetry ablation. It validates "
            "that predictions can be converted into response tags and that the "
            "`minimal_behavior` path can emit observable intervention telemetry. It does "
            "not prove win-rate improvement or gameplay quality improvement.",
            "",
            "Prediction metrics summarize `opponent_prediction` events. Response-tag "
            "metrics summarize `strategy_response` and `strategy_switch` events. "
            "Intervention metrics summarize `minimal_behavior_intervention` events.",
            "",
            "## Known Limitations",
            "",
        ]
    )
    for item in summary["known_limitations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Experiment", "", summary["next_experiment_recommendation"], ""])
    return "\n".join(lines)


def _group_by_mode(features: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in features:
        grouped[str(item.get("opponent_model_mode") or "unknown")].append(item)
    return {mode: _summarize_items(items) for mode, items in grouped.items()}


def _group_by_bot_config(features: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in features:
        grouped[str(item.get("bot_config_id") or "unknown")].append(item)
    return {bot_config_id: _summarize_strategy_items(items) for bot_config_id, items in grouped.items()}


def _summarize_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    first_seen_values = [
        item["first_enemy_seen_time"]
        for item in items
        if item.get("first_enemy_seen_time") is not None
    ]
    return {
        "match_count": len(items),
        "status_counts": dict(Counter(item.get("match_status") for item in items)),
        "first_enemy_seen_time_avg": _average(first_seen_values),
        "observation_rush_signal_matches": sum(
            1 for item in items if item.get("observation_rush_signal_seen")
        ),
        "observation_tech_signal_matches": sum(
            1 for item in items if item.get("observation_tech_signal_seen")
        ),
        "possible_rush_signal_matches": sum(
            1 for item in items if item.get("observation_rush_signal_seen")
        ),
        "possible_tech_signal_matches": sum(
            1 for item in items if item.get("observation_tech_signal_seen")
        ),
        "prediction_rush_risk_max": max(
            (float(item.get("prediction_rush_risk_max") or 0.0) for item in items),
            default=0.0,
        ),
        "prediction_tech_risk_max": max(
            (float(item.get("prediction_tech_risk_max") or 0.0) for item in items),
            default=0.0,
        ),
        "prediction_confidence_max": max(
            (float(item.get("prediction_confidence_max") or 0.0) for item in items),
            default=0.0,
        ),
        "prediction_signals_non_empty_count": sum(
            int(item.get("prediction_signals_non_empty_count") or 0) for item in items
        ),
        "prediction_recommended_response_tags_count": sum(
            int(item.get("prediction_recommended_response_tags_count") or 0) for item in items
        ),
        "visible_enemy_units_max": max(
            (int(item.get("visible_enemy_units_max") or 0) for item in items), default=0
        ),
        "visible_enemy_structures_max": max(
            (int(item.get("visible_enemy_structures_max") or 0) for item in items),
            default=0,
        ),
    }


def _summarize_strategy_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    base = _summarize_items(items)
    return {
        **base,
        "opponent_model_modes": sorted(
            {str(item.get("opponent_model_mode")) for item in items if item.get("opponent_model_mode")}
        ),
        "intervention_modes": sorted(
            {str(item.get("intervention_mode")) for item in items if item.get("intervention_mode")}
        ),
        "selected_response_tag_count": sum(
            int(item.get("selected_response_tag_count") or 0) for item in items
        ),
        "strategy_switch_count": sum(
            int(item.get("strategy_switch_count") or 0) for item in items
        ),
        "defensive_posture_count": sum(
            int(item.get("defensive_posture_count") or 0) for item in items
        ),
        "continue_scouting_count": sum(
            int(item.get("continue_scouting_count") or 0) for item in items
        ),
        "tech_alert_count": sum(int(item.get("tech_alert_count") or 0) for item in items),
        "minimal_behavior_intervention_count": sum(
            int(item.get("minimal_behavior_intervention_count") or 0) for item in items
        ),
        "minimal_behavior_active_count": sum(
            int(item.get("minimal_behavior_active_count") or 0) for item in items
        ),
        "minimal_behavior_skipped_count": sum(
            int(item.get("minimal_behavior_skipped_count") or 0) for item in items
        ),
    }


def _prediction_timeline_summary(features: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "match_id": item.get("match_id"),
            "bot_config_id": item.get("bot_config_id"),
            "opponent_id": item.get("opponent_id"),
            "first_enemy_seen_time": item.get("first_enemy_seen_time"),
            "prediction_rush_risk_max": item.get("prediction_rush_risk_max"),
            "prediction_tech_risk_max": item.get("prediction_tech_risk_max"),
            "prediction_confidence_max": item.get("prediction_confidence_max"),
            "selected_response_tag_count": item.get("selected_response_tag_count"),
            "strategy_switch_count": item.get("strategy_switch_count"),
            "minimal_behavior_intervention_count": item.get(
                "minimal_behavior_intervention_count"
            ),
        }
        for item in sorted(
            features,
            key=lambda value: (
                str(value.get("bot_config_id") or ""),
                str(value.get("opponent_id") or ""),
                str(value.get("match_id") or ""),
            ),
        )
    ]


def _average(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 3)


def _rule_based_signal_sample(features: list[dict[str, Any]]) -> dict[str, Any] | None:
    for item in features:
        if item.get("opponent_model_mode") != "rule_based":
            continue
        sample = item.get("prediction_signal_sample")
        if sample:
            return sample
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Build opponent-model ablation report.")
    parser.add_argument("--evaluation-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id")
    parser.add_argument(
        "--match-dir",
        action="append",
        dest="match_dirs",
        help="Explicit current-run match directory. Repeat to isolate a report run.",
    )
    args = parser.parse_args()
    summary = build_ablation_summary(
        args.evaluation_dir,
        args.output_dir,
        run_id=args.run_id,
        match_dirs=args.match_dirs,
    )
    print(
        f"opponent-model ablation report generated: {args.output_dir} "
        f"({summary['match_count']} matches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
