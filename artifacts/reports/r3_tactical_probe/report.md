# R3 Tactical Probe Report

Date: 2026-04-25
Task: `task_011_real_tactical_probe`

## Run

- run dir: `data/logs/evaluation/r3_tactical_probe/reallaunch-bb2aed30`
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

- `max_own_army_count = 10`
- `attack_order_count = 350`
- `defend_order_count = 125`
- `army_rally_count = 992`
- `combat_event_detected_count = 0`
- `combat_event_skipped_count = 2401`
- `unit_created_detected_count = 10`
- `army_presence_changed_count = 10`

Interpretation:

- at least one legal tactical order clearly occurred in a real match with `own_army_count > 0`
- both `defend_order` and `attack_order` appeared in telemetry
- `combat_event_detected` never fired
- the final combat-event payload stayed `planning_signal_without_execution_evidence`
- this means tactical planning is active, but executed friendly-combat evidence is still absent in the current telemetry contract

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-visible friendly combat summary: replay is saved, but this turn does not produce an independent replay-backed statement about friendly combat

## Failure Classification

Current best fit:

- `logic_failure`

Reasoning:

- minimum tactical order evidence exists
- but no executed friendly-combat evidence was recorded
- the strongest remaining gap is not army existence; it is that the tactical execution / combat-evidence path still does not materialize beyond planning telemetry

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
- the last combat-event payload remained `planning_signal_without_execution_evidence`

## Stretch Gate

`failed`

Reason:

- while both defend and attack planning signals appeared, the probe still does not establish executed friendly combat or a replay-backed contact narrative

## What This Proves

- this rerun is valid L3 evidence
- at least one legal tactical order occurred in a real match while `own_army_count > 0`
- R3 minimum tactical-order evidence is now available for checkpoint review

## What This Does Not Prove

- it does not validate friendly combat
- it does not prove replay-backed contact
- it does not prove target-level tactical stability
- it does not allow `attack_order` or `defend_order` alone to be treated as executed-combat evidence
