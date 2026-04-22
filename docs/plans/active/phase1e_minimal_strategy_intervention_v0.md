# Plan: Phase 1E Minimal Strategy Intervention V0

Status: completed on 2026-04-21.

## Summary

Phase 1E moves the project from prediction-only opponent modeling to the first
minimal, explainable, reversible strategy intervention. The goal is not win-rate
improvement. The goal is to prove that opponent-model predictions can be
consumed by `StrategyManager`, converted into response tags, lightly influence
survival-baseline behavior, and be measured in telemetry and reports.

## Goal

Establish a minimal strategy-intervention experiment loop:

- `opponent_prediction` is consumed by `StrategyManager`;
- `selected_response_tag` is produced and recorded;
- `strategy_switch_reason` is produced and recorded;
- `intervention_mode` can be switched between `none`, `tag_only`, and
  `minimal_behavior`;
- minimal behavior changes are observable in telemetry;
- null, prediction-only, and intervention modes can be compared without
  claiming unsupported performance gains.

## Scope

Allowed Phase 1E work:

- strategy response data shape;
- intervention config schema;
- tag-only `StrategyManager` response selection;
- `strategy_response` / `strategy_switch` telemetry;
- a minimal behavior intervention entry point;
- very thin behavior changes:
  - `defensive_posture` influences existing army-defense target preference;
  - `continue_scouting` influences scout persistence;
  - `tech_alert` may remain telemetry-only;
- feature extraction and reporting for strategy responses;
- small real local SC2 probes and a small ablation at explicit L3 gates.

## Non-goals

Forbidden in Phase 1E:

- complex build order;
- gateway production;
- gas, tech, or full army production;
- expansion;
- SMAC;
- LLM control or replay summary;
- world-model-lite;
- replay imitation learning;
- importing `research/` code into `src/sc2bot/`;
- claiming win-rate or gameplay-quality improvement without evidence.

## Proposed Config Shape

```yaml
opponent_model:
  mode: rule_based
  intervention_mode: none  # none | tag_only | minimal_behavior
  rush_risk_threshold: 0.5
  tech_risk_threshold: 0.5
  low_information_confidence_threshold: 0.25
  low_information_game_time_threshold: 90.0
```

Mode meanings:

- `none`: prediction-only. Predictions are recorded but do not produce strategy
  responses.
- `tag_only`: `StrategyManager` selects and records response tags but does not
  change gameplay.
- `minimal_behavior`: selected response tags may trigger the approved thin
  behavior changes.

## Minimal Response Rules

### low_information

Condition:

- prediction confidence is low, or game time passes a configured threshold
  without useful enemy information.

Response:

- `selected_response_tag: continue_scouting`
- `strategy_switch_reason: low_information`
- behavior: keep or extend scout persistence only.

### rush_risk

Condition:

- `rush_risk >= rush_risk_threshold`

Response:

- `selected_response_tag: defensive_posture`
- `strategy_switch_reason: rush_risk_high`
- behavior: existing army units prefer home / townhall defense positioning.

### tech_risk

Condition:

- `tech_risk >= tech_risk_threshold`

Response:

- `selected_response_tag: tech_alert`
- `strategy_switch_reason: tech_risk_high`
- behavior: telemetry-only in Phase 1E unless a later task explicitly approves
  a minimal non-production response.

## Verification Levels

- `L0`: static/code check. Files, interfaces, or configs exist.
- `L1`: unit test. Synthetic prediction or fake observation verifies logic.
- `L2`: dry telemetry. Dry path writes expected telemetry without SC2.
- `L3`: real telemetry. A real SC2 local match contains the target telemetry.

Do not treat a task as real-match validated unless `actual_validation_level` is
`L3`, `data_source` is real match telemetry, and `evidence_paths` records the
real output directory or telemetry file.

## Documentation

Each completed task must update:

- `docs/plans/active/phase1e_task_queue.yaml`;
- `docs/handoffs/latest.md`.

Milestone closeout must update:

- `docs/context/current_status.md`;
- `docs/context/validated_findings.md`;
- `docs/context/open_hypotheses.md`;
- `docs/commands/common_commands.md`;
- `docs/commands/verification_matrix.md`;
- `docs/handoffs/latest.md`.

## Assumptions

- Phase 1D remains the accepted prediction-only baseline.
- Every Phase 1E task is manually triggered and stops after one queue item.
- Real SC2 validation appears only in tasks that explicitly require L3.
- Minimal behavior interventions must be config-gated and easy to disable.
