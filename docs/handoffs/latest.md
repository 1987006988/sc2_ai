# Handoff: checkpoint_F_adaptive_research_gate

Date: 2026-04-25

## Executed Work

- `task_017_null_vs_adaptive_paired_evaluation`
- `checkpoint_F_adaptive_research_gate`

## Status

- `task_017`: `completed`
- `checkpoint_F`: `completed`

## Validation

- `task_017` validation level achieved: `L4`
- `task_017` data source: `prior real paired SC2 outputs`
- `task_017` capability validation status: `capability_validated_target`
- `checkpoint_F` validation level achieved: `L5`
- `checkpoint_F` capability validation status: `capability_validated_target`

## Verification Inputs

- `artifacts/reports/r5_paired_adaptive_eval/task_016_static_validation.md`
- invalid control context:
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_20260425/summary.json`
- accepted control:
  - `data/logs/evaluation/r5_paired_adaptive_eval/control/r5_paired_control_zerg_clean_20260425/summary.json`
- diagnostic clean treatment:
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_clean_20260425/summary.json`
- accepted retuned treatment:
  - `data/logs/evaluation/r5_paired_adaptive_eval/treatment/r5_paired_treatment_zerg_retuned_20260425/summary.json`
- paired report:
  - `artifacts/reports/r5_paired_adaptive_eval/report.md`

## Task 017 Result

- minimum gate result: `passed`
- target gate result: `passed`
- stretch gate status: `failed`

Accepted paired comparison:

- control clean: `1/3` wins
- treatment retuned: `2/3` wins

Behavior delta:

- control:
  - `adaptive_gate_applied = 0`
- treatment retuned:
  - `adaptive_gate_applied = 682`
  - `worker_scout_persistence_applied = 679`
  - selected response tag concentrated on `continue_scouting`

Interpretation:

- invalid polluted control output was excluded
- initial clean treatment showed behavior change without benefit and remains
  diagnostic-only context
- the accepted treatment result uses the same adaptive feature after a same-feature
  small-step retune
- accepted behavior delta and accepted outcome delta now move in the same
  direction on the matched Easy Zerg slice

## Checkpoint F Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `actual_game_time_sufficient = yes`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = project_core_goal_reached`

## What This Proves

- the project now has an accepted Level 1 playable baseline
- the project now has one accepted adaptive research contribution in real SC2
- the validated adaptive contribution is a sparse-scout gating layer whose
  accepted effect is established on one matched Easy Zerg slice

## What This Does Not Prove

- it does not prove broader-pool generalization
- it does not prove Medium-opponent strength
- it does not prove ladder competitiveness
- it does not prove a second adaptive feature

## Files Changed

- `artifacts/reports/r5_paired_adaptive_eval/report.md`
- `artifacts/reports/checkpoints/checkpoint_F_adaptive_research_gate.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/handoffs/latest.md`
- `docs/context/current_status.md`

## Blockers

- no blocker remains before `checkpoint_F`
- broader extension remains unvalidated, but it is not a blocker to the core
  project goal already accepted by `checkpoint_F`

## Next Pending Task

- `project_core_goal_reached`

## Stop

This turn did not execute any post-`checkpoint_F` extension task.
No new SC2 run was required in this turn; the phase closeout used already
collected valid paired evidence.
