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
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/summary.json`
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

`task_014` then repaired the dominant failure class and expanded the evidence:

- repair scope: increase baseline Gateway target from `1` to `2`
- focused Terran rerun: `2/2` wins
- first Zerg/Protoss confirmation attempt: `invalid_evidence`
  - cause: launch shell missing `SC2PATH`
- corrected Zerg/Protoss confirmation rerun:
  - Zerg easy: `0/2` wins
  - Protoss easy: `0/2` wins
  - no prerequisite regression found after the corrected launch

## Checkpoint Decision

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = passed`
- `actual_game_time_sufficient = yes`
- `capability_validation_status = capability_validated_target`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = task_016_integrate_single_adaptive_gating_layer`

## Interpretation

This checkpoint still accepts that the baseline has crossed the minimum R4 line:

- it is no longer just a survival scaffold
- no fatal prerequisite regression remains in the reviewed evidence
- the repaired baseline can produce uncontested wins on an easy Terran slice

This checkpoint now accepts full Level 1 target:

- the original easy-slice batch exposed the failure class clearly
- the first focused repair converted the Terran slice to repeated wins
- the second focused repair lifted the remaining Zerg/Protoss confirmation
  slice to `3/4` wins
- the designated easy slice now has repeated real wins with matching gameplay
  evidence and no prerequisite regression

## What This Proves

- Level 1 playable baseline is now accepted
- the baseline is stable enough to act as the control for the adaptive paired
  evaluation phase

## What This Does Not Prove

- it does not prove perfect win coverage on every easy-race repeat
- it does not prove ladder competitiveness
- it does not by itself validate the adaptive research feature
