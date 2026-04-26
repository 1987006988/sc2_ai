# R7 Checkpoint M: Strong Bot Gate

Date: 2026-04-27

## Reviewed Tasks

- `r7_task_004_acquire_and_license_audit_selected_strong_bot`
- `r7_task_005_run_selected_strong_bot_and_collect_seed_data`

## Evidence Paths

- `third_party/strong_bots/README.md`
- `configs/research/r7_selected_strong_bot.yaml`
- `artifacts/reports/r7_strong_bot_acquisition/report.md`
- `artifacts/reports/r7_strong_bot_acquisition/local_run_report.md`
- `data/r7/strong_bot_seed/manifest.json`
- `artifacts/reports/checkpoints/r7_checkpoint_M_strong_bot_gate.md`

## Gate Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = r7_task_007_materialize_teacher_replay_dataset`

## Why It Passes

1. a selected strong source was actually acquired and version-pinned
2. the source license is permissive for the intended near-term research use
3. the source includes documented runtime paths plus a replay corpus
4. a valid seed replay corpus was materialized and can drive teacher-data work

## Why Stretch Fails

1. no backup candidate was acquired this turn
2. no direct local DI-star match was executed
3. no machine-local strength comparison was performed

## Claim Boundary

This checkpoint accepts:

1. teacher-source viability
2. acquisition and license audit completeness
3. seed replay corpus materialization

This checkpoint does not accept:

1. full online substrate viability
2. strong-substrate intervention readiness
3. outcome claims against external bots

## Invalid Evidence Excluded

1. no downloaded model performance is claimed
2. no unaudited third-party runtime result is mixed into acceptance
3. no fabricated local run is used in place of real replay-corpus evidence
