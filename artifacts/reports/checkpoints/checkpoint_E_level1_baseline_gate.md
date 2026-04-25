# Checkpoint E Level 1 Baseline Gate

Date: 2026-04-25
Checkpoint: `checkpoint_E_level1_baseline_gate`

## Reviewed Tasks

- `task_013_baseline_easy_pool_batch_evaluation`
- `task_014_baseline_repair_or_confirmation`

## Evidence Paths

- `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/summary.json`
- `artifacts/reports/r4_baseline_easy_pool/report.md`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/summary.json`
- `artifacts/reports/r4_baseline_repair_or_confirmation/report.md`
- `artifacts/reports/checkpoints/checkpoint_E_level1_baseline_gate.md`

## Evidence Summary

`task_013` established the full easy-slice baseline picture:

- valid easy-slice batch size: `6`
- outcomes:
  - Terran easy: `0/2` wins
  - Zerg easy: `0/2` wins
  - Protoss easy: `0/2` wins
- no prerequisite regression was found

`task_014` then repaired the dominant failure class in a focused slice:

- repair scope: increase baseline Gateway target from `1` to `2`
- focused rerun slice: `builtin_easy_terran`, `2` repeats
- focused rerun outcomes: `2/2` wins

## Checkpoint Decision

- `minimum_gate_passed = true`
- `target_gate_passed = false`
- `stretch_gate_status = failed`
- `actual_game_time_sufficient = yes`
- `capability_validation_status = capability_validated_minimum`
- `failure_class = stability_failure`
- `decision = repair_and_rerun`
- `next_allowed_task = task_014_baseline_repair_or_confirmation`

## Interpretation

This checkpoint accepts that the baseline has crossed the minimum R4 line:

- it is no longer just a survival scaffold
- no fatal prerequisite regression remains in the reviewed evidence
- a focused repair can now produce uncontested real wins on an easy slice

But this checkpoint does **not** accept full Level 1 target yet:

- the original easy-slice batch was uniformly defeat
- the focused repair only reconfirmed the Terran slice
- Zerg and Protoss have not yet been revalidated after the repair
- the designated easy slice as a whole still lacks repeated-outcome coverage

## What This Proves

- Level 1 baseline minimum is now accepted
- the remaining R4 blocker is slice-level stability and repeated-outcome coverage

## What This Does Not Prove

- it does not accept full Level 1 target yet
- it does not prove repeated wins across the designated easy slice
- it does not justify entering adaptive paired evaluation
