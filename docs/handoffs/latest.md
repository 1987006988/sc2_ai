# Handoff: task_008_real_army_presence_probe

Date: 2026-04-25

## Executed Task

- `task_008_real_army_presence_probe`

## Status

- `completed`

## Validation

- validation level achieved: `L3`
- data source: `new real SC2 local match output`
- capability validation status: `capability_validated_minimum`

## Files Changed

- `data/logs/evaluation/r2_army_presence_probe/summary.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match_result.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/telemetry/events.jsonl`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match.SC2Replay`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/preflight.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/replay_metadata.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/launch_path_diagnostics.json`
- `artifacts/reports/r2_army_presence_probe/report.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/handoffs/latest.md`

## Verification Commands And Results

- real probe command:
  - `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& <r2_army_presence_probe.ps1>"`
- result:
  - run completed with `status = max_game_time_reached`
  - `result = Result.Defeat`
  - `runtime_max_game_loop = 9600`
  - `requested_game_time_limit_seconds = 459`
  - `max_game_time = 428.5714285714286`
- artifact completeness:
  - `summary.json`: present
  - `match_result.json`: present
  - `telemetry/events.jsonl`: present
  - `match.SC2Replay`: present
  - `preflight.json`: present
  - `replay_metadata.json`: present
  - `launch_path_diagnostics.json`: present

## Key Probe Counts

- `train_command_issued = 11`
- `combat_unit_production_success = 11`
- `queued_after_train = 11`
- `queued_after_train_zero_delta = 11`
- `unit_created_detected = 10`
- `unit_alive_after_short_window = 0`
- `army_presence_changed = 10`
- `max_own_army_count = 10`
- `max_documented_own_army_count = 10`
- `max_legacy_own_army_count = 0`
- `max_combat_unit_count = 0`
- `attack_order_count = 334`

## Current Best Failure Classification

- `state_extraction_or_army_classification_failure`

Reason:

- `queued_after_train` remained zero-delta in the `already_pending(...)` channel
- but `on_unit_created(...)` still fired 10 times for zealots
- documented `own_army_count` rose to 10
- `army_presence_changed` fired 10 times
- `attack_order` was emitted with `own_army_count = 10`
- the remaining discrepancy is therefore in the legacy / classification path, not in broad unit materialization

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-backed corroboration status:
  - replay is saved, but this turn did not produce an independent replay-backed statement about friendly combat-unit appearance

## Minimum / Target / Stretch

- minimum gate result: `passed_with_replay_review_caveat`
- target gate result: `failed`
- stretch gate status: `failed`

## What This Proves

- this rerun is valid L3 evidence
- friendly combat units were created in the real match
- documented `own_army_count` rose above zero to 10
- the dominant blocker has narrowed from broad production failure to a legacy state extraction / army classification mismatch

## What This Does Not Prove

- it does not complete replay-backed corroboration
- it does not prove target-level stability
- it does not prove the legacy army-count channel is safe
- it does not execute or pass `checkpoint_C_army_core_gate`

## Evidence Paths

- `data/logs/evaluation/r2_army_presence_probe/summary.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match_result.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/telemetry/events.jsonl`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match.SC2Replay`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/preflight.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/replay_metadata.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/launch_path_diagnostics.json`
- `artifacts/reports/r2_army_presence_probe/report.md`

## Blockers

- `checkpoint_C_army_core_gate` still needs to review the replay caveat and the legacy-classification mismatch
- tactical progression remains blocked until checkpoint review

## Next Pending Task

- `checkpoint_C_army_core_gate`

## Stop

This turn did not execute `checkpoint_C_army_core_gate`.
