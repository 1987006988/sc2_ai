# Checkpoint D Tactical Core Gate

Date: 2026-04-25
Checkpoint: `checkpoint_D_tactical_core_gate`

## Reviewed Tasks

- `task_010_rewrite_defend_attack_transition_logic`
- `task_011_real_tactical_probe`

## Evidence Paths

- `data/logs/evaluation/r3_tactical_probe/summary.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match_result.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/telemetry/events.jsonl`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/match.SC2Replay`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-1acc7c1f/launch_path_diagnostics.json`
- `artifacts/reports/r3_tactical_probe/report.md`
- `artifacts/reports/checkpoints/checkpoint_D_tactical_core_gate.md`

## Evidence Summary

Real probe validity:

- `status = max_game_time_reached`
- `result = Result.Defeat`
- `runtime_max_game_loop = 9600`
- artifact set is complete

Load-bearing tactical counts:

- `max_own_army_count = 9`
- `attack_order_count = 309`
- `defend_order_count = 155`
- `army_rally_count = 1001`
- `combat_event_detected_count = 0`
- `tactical_order_execution_count = 2401`
- `tactical_execution_applied_count = 0`
- `tactical_execution_skipped_count = 2401`
- `unit_created_detected_count = 10`
- `army_presence_changed_count = 10`

Execution-layer boundary:

- legal tactical orders clearly occurred
- documented/planning state saw army presence
- execution-layer telemetry stayed at `outcome = skipped`
- dominant execution reason remained `no_army_available`
- final combat payload remained `planning_signal_without_execution_evidence`

## Checkpoint Decision

- `minimum_gate_passed = true`
- `target_gate_passed = false`
- `stretch_gate_status = failed`
- `actual_game_time_sufficient = yes`
- `capability_validation_status = capability_validated_minimum`
- `failure_class = logic_failure`
- `decision = repair_and_rerun`
- `next_allowed_task = task_010_rewrite_defend_attack_transition_logic`

## Interpretation

This checkpoint accepts that R3 is no longer diagnostic-only:

- at least one legal tactical order occurred in a valid real probe
- `own_army_count > 0` held during tactical planning
- tactical minimum therefore passes

This checkpoint does not accept tactical target success:

- no executed friendly-combat evidence was validated
- `combat_event_detected_count = 0`
- `tactical_execution_applied_count = 0`
- replay-backed corroboration is still missing

The phase-level failure class remains `logic_failure`, but the narrower
sub-diagnosis is:

- documented/planning army exists
- execution-layer army visibility or executability still fails

## What This Proves

- tactical minimum is accepted
- R3 may continue only through repair and rerun
- the blocker is no longer army existence itself
- the blocker is now execution-layer evidence semantics and executable army visibility

## What This Does Not Prove

- it does not validate friendly combat
- it does not justify baseline batch evaluation
- it does not allow `attack_order`, `defend_order`, or `army_rally` counts to stand in for executed combat
- it does not prove replay-backed contact
