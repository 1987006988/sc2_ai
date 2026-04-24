# Handoff: task_011_real_tactical_probe

Date: 2026-04-25

## Executed Task

- `task_011_real_tactical_probe`

## Status

- `completed`

## Validation

- validation level achieved: `L3`
- data source: `new real SC2 local match output`
- capability validation status: `capability_validated_minimum`

## Files Changed

- `data/logs/evaluation/r3_tactical_probe/summary.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match_result.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/telemetry/events.jsonl`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match.SC2Replay`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/preflight.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/replay_metadata.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/launch_path_diagnostics.json`
- `artifacts/reports/r3_tactical_probe/report.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/handoffs/latest.md`

## Verification Commands And Results

- real probe command:
  - `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& <r3_tactical_probe.ps1>"`
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

- `max_own_army_count = 9`
- `attack_order_count = 309`
- `defend_order_count = 155`
- `army_rally_count = 1001`
- `combat_event_detected_count = 0`
- `combat_event_skipped_count = 2401`
- `tactical_order_execution_count = 2401`
- `tactical_execution_applied_count = 0`
- `tactical_execution_skipped_count = 2401`
- `unit_created_detected_count = 10`
- `army_presence_changed_count = 10`

## Current Best Failure Classification

- `state_extraction_or_army_classification_failure`

Reason:

- legal tactical orders clearly occurred
- `own_army_count > 0` held during those orders
- execution-layer telemetry now exists and shows the next failure boundary directly
- but every `tactical_order_execution` remained `outcome = skipped` with
  `execution_reason = no_army_available`
- the remaining gap is therefore the documented-vs-executable army mismatch,
  not broad tactical planning failure

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-backed corroboration status:
  - replay is saved, but this turn did not produce an independent replay-backed statement about friendly combat

## Minimum / Target / Stretch

- minimum gate result: `passed_with_replay_review_caveat`
- target gate result: `failed`
- stretch gate status: `failed`

## What This Proves

- this rerun is valid L3 evidence
- at least one legal tactical order occurred in a real match while `own_army_count > 0`
- the new execution-layer telemetry made the remaining blocker more precise
- the dominant blocker is now explicitly the documented-vs-executable army mismatch

## What This Does Not Prove

- it does not validate friendly combat
- it does not prove replay-backed contact
- it does not prove target-level tactical stability
- it does not allow `attack_order` or `defend_order` alone to be treated as executed-combat evidence

## Evidence Paths

- `data/logs/evaluation/r3_tactical_probe/summary.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match_result.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/telemetry/events.jsonl`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match.SC2Replay`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/preflight.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/replay_metadata.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/launch_path_diagnostics.json`
- `artifacts/reports/r3_tactical_probe/report.md`

## Blockers

- executed friendly-combat evidence is still absent
- replay-backed corroboration is still pending
- `checkpoint_D_tactical_core_gate` should now review the narrower
  documented-vs-executable army mismatch

## Next Pending Task

- `checkpoint_D_tactical_core_gate`

## Stop

This turn did not execute `checkpoint_D_tactical_core_gate`.
