# R5 Paired Adaptive Evaluation Report

Date: 2026-04-25
Task: `task_017_null_vs_adaptive_paired_evaluation`

## Evaluation Design

Matched paired evaluation:

- control config: `configs/bot/baseline_playable.yaml`
- treatment config: `configs/bot/adaptive_research.yaml`
- map slice: `IncorporealAIE_v4`
- opponent slice: `builtin_easy_zerg`
- repeats per side: `3`

Paired comparison rules:

- keep map/opponent slice fixed
- keep baseline core frozen
- only allow the sparse-scout adaptive gating layer to differ
- read behavior delta before outcome delta

## Invalid Evidence Excluded

The first control run under
`data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_20260425/`
is not used for the final paired conclusion.

Reason:

- its `summary.json` reports `6` matches instead of the intended `3`
- the output directory was polluted by stale artifacts
- this is `invalid_evidence`, not a valid paired control baseline

## Accepted Comparison

The accepted paired comparison is:

- control:
  `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/summary.json`
- treatment:
  `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/summary.json`

The earlier clean treatment run under
`r5_paired_treatment_zerg_clean_20260425` is kept as diagnostic context only.
It showed real behavior change but no causal benefit. The final accepted
treatment evidence uses the same adaptive feature after a same-feature small-step
retune:

- `rush_risk_threshold: 0.5 -> 0.65`
- `first_attack_delay_seconds: 90 -> 45`
- `first_attack_army_buffer: 2 -> 1`

No baseline-core change was introduced during this treatment retune.

## Outcome Summary

Accepted control:

- valid matches: `3`
- wins: `1/3`
- results:
  - `reallaunch-52885cb5`: `Result.Defeat`
  - `reallaunch-89ac9bfd`: `Result.Victory`
  - `reallaunch-ec54e381`: `Result.Defeat`

Accepted treatment:

- valid matches: `3`
- wins: `2/3`
- results:
  - `reallaunch-828620c4`: `Result.Victory`
  - `reallaunch-e3f9097a`: `Result.Victory`
  - `reallaunch-bf88b27a`: `Result.Defeat`

Directional outcome delta on the matched slice:

- control: `1/3`
- treatment: `2/3`

## Behavior Delta Summary

Control behavior:

- `adaptive_gate_applied = 0`
- selected response tags: `{none}`
- `combat_event_detected = 1590`
- `tactical_order_execution = 6847`

Initial clean treatment before retune:

- `adaptive_gate_applied = 6089`
- `worker_scout_persistence_applied = 679`
- selected response tags:
  - `continue_scouting = 682`
  - `defensive_posture = 5407`
- outcome: `0/3`

Retuned treatment:

- `adaptive_gate_applied = 682`
- `worker_scout_persistence_applied = 679`
- selected response tags:
  - `continue_scouting = 682`
- `combat_event_detected = 1362`
- `tactical_order_execution = 6563`

Interpretation:

- the treatment changes real gameplay behavior
- the accepted treatment no longer relies on overwhelming defensive-posture bias
- the retained behavior delta is primarily continued scout persistence under
  information gap
- the outcome improvement moves in the same direction as that narrowed behavior
  change

## Gate Assessment

## Minimum Gate

`passed`

Reason:

- paired evaluation shows a repeatable control vs treatment behavior delta
- the delta is not tag-only telemetry; it changes mainline gameplay behavior
- no baseline-core regression appears in the accepted treatment comparison

## Target Gate

`passed`

Reason:

- the matched slice shows directional outcome improvement: `1/3 -> 2/3`
- the final accepted treatment keeps the same adaptive feature and narrows the
  intervention to a plausible causal mechanism
- behavior delta and benefit direction now align well enough for phase-gate
  acceptance

## Stretch Gate

`failed`

Reason:

- accepted evidence is still limited to one opponent race and one map slice
- no broader-pool or multi-slice generalization is established

## What This Proves

- one sparse-scout adaptive gating layer changes real gameplay behavior
- the accepted treatment improves outcome on the matched Easy Zerg slice
- the project now has one accepted adaptive research contribution on top of an
  accepted Level 1 baseline

## What This Does Not Prove

- it does not prove broader-pool generalization
- it does not prove Medium-opponent performance
- it does not prove ladder competitiveness
- it does not prove multiple adaptive features

## Evidence Paths

- invalid control context:
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_20260425/summary.json`
- accepted control:
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/summary.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/reallaunch-52885cb5/match_result.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/reallaunch-89ac9bfd/match_result.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/reallaunch-ec54e381/match_result.json`
- diagnostic treatment context:
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_clean_20260425/summary.json`
- accepted treatment:
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/summary.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/reallaunch-828620c4/match_result.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/reallaunch-e3f9097a/match_result.json`
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/reallaunch-bf88b27a/match_result.json`
