# R3 Tactical Probe Report

Date: 2026-04-25
Task: `task_011_real_tactical_probe`

## Run

- run dir: `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f`
- config: `configs/bot/baseline_playable.yaml`
- opponent: `builtin_easy_terran`
- map: `incorporeal_aie_v4`

## Artifact Completeness

- `summary.json`: present
- `match_result.json`: present
- `telemetry/events.jsonl`: present
- `match.SC2Replay`: present
- `preflight.json`: present
- `replay_metadata.json`: present
- `launch_path_diagnostics.json`: present

## Key Findings

Fair opportunity window was reached:

- `max_game_time = 428.5714285714286`
- `runtime_max_game_loop = 9600`
- `requested_game_time_limit_seconds = 459`

Tactical-order signals:

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

Interpretation:

- at least one legal tactical order clearly occurred in a real match with `own_army_count > 0`
- both `defend_order` and `attack_order` appeared in planning telemetry
- `tactical_order_execution` also ran on every step
- but every execution-layer event stayed `outcome = skipped` with `execution_reason = no_army_available`
- `combat_event_detected` never fired
- the key discrepancy is now explicit: documented/planning state sees army presence, while the execution layer still sees no executable `self.army`

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-visible friendly combat summary: replay is saved, but this turn does not produce an independent replay-backed statement about friendly combat

## Failure Classification

Current best fit:

- `state_extraction_or_army_classification_failure`

Reasoning:

- minimum tactical-order evidence exists
- documented `own_army_count` rose above zero
- but execution-layer telemetry still reports `no_army_available`
- the strongest remaining gap is now the mismatch between documented army existence and legacy executable army visibility, not broad tactical logic failure

## Minimum Gate

`passed_with_replay_review_caveat`

Reason:

- a legal `defend_order` or `attack_order` occurred in a valid real probe
- `own_army_count > 0` held during those orders
- replay artifact exists, but replay-backed corroboration was not completed in this turn

## Target Gate

`failed`

Reason:

- `friendly combat` was not validated
- `combat_event_detected_count = 0`
- `tactical_execution_applied_count = 0`
- the execution layer still could not act on the documented army signal

## Stretch Gate

`failed`

Reason:

- the probe still does not establish executed friendly combat or a replay-backed contact narrative
- baseline batch would still be premature

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
