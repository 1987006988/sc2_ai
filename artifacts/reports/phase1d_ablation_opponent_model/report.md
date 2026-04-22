# Phase 1D Opponent Model Ablation V0

- Run timestamp: `2026-04-20T15:45:53.353572+00:00`
- Run id: `phase1d_task11c_latest_2x2`
- Evaluation dir: `data/logs/evaluation/phase1d_ablation_opponent_model`
- Output scope: `explicit_match_dirs`
- Match count: `4`
- Maps: incorporeal_aie_v4
- Opponents: builtin_easy_terran, builtin_easy_zerg
- Bot configs: null, rule_based

## Status Counts

- `max_game_time_reached`: 4

## Historical Results Excluded

- Historical match directories excluded from this summary: `4`

## Opponent Model Mode Comparison

### null

- Matches: `2`
- First enemy seen average: `40.268`
- Observation rush signal matches: `1`
- Observation tech signal matches: `2`
- Prediction rush risk max: `0.0`
- Prediction tech risk max: `0.0`
- Prediction confidence max: `0.0`
- Prediction non-empty signal events: `0`
- Prediction recommended response tag count: `0`
- Max visible enemy units: `23`
- Max visible enemy structures: `6`

### rule_based

- Matches: `2`
- First enemy seen average: `40.446`
- Observation rush signal matches: `0`
- Observation tech signal matches: `2`
- Prediction rush risk max: `0.1`
- Prediction tech risk max: `0.5`
- Prediction confidence max: `0.55`
- Prediction non-empty signal events: `683`
- Prediction recommended response tag count: `1500`
- Max visible enemy units: `22`
- Max visible enemy structures: `6`

## Rule-Based Prediction Signal Sample

- Match dir: `data/logs/evaluation/phase1d_ablation_opponent_model/reallaunch-10906834`
- Opening type: `production_seen`
- Rush risk: `0.1`
- Tech risk: `0.05`
- Confidence: `0.45`
- Prediction mode: `prediction_only`
- Signals: `production_structure`
- Recommended response tags: `prediction_only`

## Interpretation

This is a prediction-only ablation. It validates configuration switching, prediction telemetry, feature extraction, and reporting. It does not prove that the rule-based opponent model improves win rate or gameplay quality.

Observation-derived signals are raw scouting telemetry signals. Prediction-derived signals come only from `opponent_prediction` events. Observation signals should not be treated as opponent-model prediction quality.

## Known Limitations

- This is a prediction-only ablation.
- The rule-based model does not change gameplay behavior.
- This report does not prove win-rate improvement.
- Observation-derived signals come from scouting telemetry and are not opponent-model predictions.

## Next Experiment

Use the extracted risk signals to design a small behavior intervention, then rerun the same fixed pool.
