# R3 Tactical Probe Report

Date: 2026-04-25
Task: `task_011_real_tactical_probe`

## Run

- run dir: `data/logs/evaluation/r3_tactical_probe/reallaunch-d7ce499f`
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

- `status = max_game_time_reached`
- `result = Result.Defeat`
- `runtime_max_game_loop = 9600`
- `requested_game_time_limit_seconds = 459`

Tactical-order and execution-layer signals:

- `max_own_army_count = 9`
- `max_documented_own_army_count = 9`
- `max_execution_army_count = 9`
- `max_execution_idle_army_count = 6`
- `attack_order_count = 217`
- `defend_order_count = 269`
- `army_rally_count = 977`
- `combat_event_detected_count = 13`
- `combat_event_skipped_count = 4789`
- `tactical_order_execution_count = 2401`
- `tactical_execution_applied_count = 878`
- `tactical_execution_skipped_count = 1523`
- `unit_created_detected_count = 10`
- `army_presence_changed_count = 10`

Interpretation:

- at least one legal tactical order clearly occurred in a real match with `own_army_count > 0`
- execution-layer telemetry is no longer stuck at `no_army_available`
- `execution_army_source = self_units_combat_fallback` confirms the new fallback path was actually exercised
- real command application now occurred:
  - `army_rally_move_applied = 865`
  - `defend_order_attack_applied = 7`
  - `attack_order_command_applied = 6`
- post-execution combat telemetry now also fired:
  - `combat_event_detected_count = 13`
  - detected reason = `execution_applied_with_enemy_contact`
- the dominant blocker from earlier R3 probes is therefore resolved:
  - execution-applied tactical behavior can now upgrade into a contact/combat-neighbor signal

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-visible friendly combat summary: replay is saved, but this turn does not produce an independent replay-backed statement about friendly combat

## Failure Classification

Current best fit:

- `none`

Reasoning:

- minimum tactical-order evidence exists
- execution-layer command application exists
- combat confirmation no longer remains stuck at planning-only
- the remaining replay caveat is non-blocking for this checkpoint, but still does not establish a replay-backed combat narrative on its own

## Minimum Gate

`passed_with_replay_review_caveat`

Reason:

- a legal `defend_order` or `attack_order` occurred in a valid real probe
- `own_army_count > 0` held during those orders
- replay artifact exists, but replay-backed corroboration was not completed in this turn

## Target Gate

`passed_with_replay_review_caveat`

Reason:

- `combat_event_detected_count = 13`
- detected reason is now `execution_applied_with_enemy_contact`
- execution-layer command application and combat-neighbor confirmation now align in telemetry
- replay-backed corroboration is still pending, so this is target evidence with a replay caveat rather than a full replay-reviewed combat narrative

## Stretch Gate

`passed`

Reason:

- tactical evidence is now strong enough to support entry into baseline batch
- no prerequisite regression was observed

## What This Proves

- this rerun is valid L3 evidence
- at least one legal tactical order occurred in a real match while `own_army_count > 0`
- execution-layer command application now occurs against executable combat units
- post-execution combat telemetry now detects `execution_applied_with_enemy_contact`
- the `self.units` combat fallback plus post-execution combat assessment resolved the R3 tactical evidence-chain blocker

## What This Does Not Prove

- it does not provide a replay-reviewed friendly combat narrative
- it does not prove replay-backed contact independent of telemetry
- it does not prove target-level tactical stability
- it does not allow `attack_order` or `defend_order` alone to be treated as executed-combat evidence
