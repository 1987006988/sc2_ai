# Checkpoint F Adaptive Research Gate

Date: 2026-04-25
Checkpoint: `checkpoint_F_adaptive_research_gate`

## Reviewed Tasks

- `task_016_integrate_single_adaptive_gating_layer`
- `task_017_null_vs_adaptive_paired_evaluation`

## Evidence Paths

- `artifacts/reports/r5_paired_adaptive_eval/task_016_static_validation.md`
- `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/summary.json`
- `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/summary.json`
- `artifacts/reports/r5_paired_adaptive_eval/report.md`
- `artifacts/reports/checkpoints/checkpoint_F_adaptive_research_gate.md`

## Evidence Summary

`task_016` moved the adaptive layer into the gameplay path:

- `BeliefState` is now a typed mainline artifact
- adaptive gating can alter scouting persistence, defensive posture, and first
  attack timing
- control and treatment remain auditable and separable

`task_017` then established a matched paired result on Easy Zerg:

- invalid polluted control run was excluded from the final conclusion
- accepted control slice: `1/3` wins
- accepted retuned treatment slice: `2/3` wins
- paired behavior delta remained present and interpretable
- accepted treatment concentrated the intervention on
  `continue_scouting` persistence rather than the earlier over-broad defensive
  bias

## Checkpoint Decision

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `actual_game_time_sufficient = yes`
- `capability_validation_status = capability_validated_target`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = project_core_goal_reached`

## Interpretation

This checkpoint accepts the core research claim at the intended phase-gate
level:

- the adaptive layer changes real gameplay behavior
- the final accepted paired slice shows benefit in the same direction as that
  behavior change
- no baseline-core regression is needed to explain the result

This checkpoint does not accept broader extension claims:

- only one opponent race and one map slice are validated
- no Medium slice is validated
- no ladder-strength claim is justified

## What This Proves

- the project now has an accepted Level 1 playable baseline
- the project now has one accepted adaptive research contribution validated in
  real SC2
- the core project goal has been reached at the planned scope

## What This Does Not Prove

- it does not prove broad generalization
- it does not prove a second adaptive contribution
- it does not prove ladder competitiveness
