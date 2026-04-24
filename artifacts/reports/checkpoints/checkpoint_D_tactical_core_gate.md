# Checkpoint D Tactical Core Gate

Date: 2026-04-25
Checkpoint: `checkpoint_D_tactical_core_gate`

## Reviewed Tasks

- `task_010_rewrite_defend_attack_transition_logic`
- `task_011_real_tactical_probe`

## Evidence Paths

- `data/logs/evaluation/r3_tactical_probe/summary.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-d7ce499f/match_result.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-d7ce499f/telemetry/events.jsonl`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-d7ce499f/match.SC2Replay`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-d7ce499f/launch_path_diagnostics.json`
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
- `max_documented_own_army_count = 9`
- `max_execution_army_count = 9`
- `max_execution_idle_army_count = 6`
- `attack_order_count = 217`
- `defend_order_count = 269`
- `army_rally_count = 977`
- `combat_event_detected_count = 13`
- `tactical_order_execution_count = 2401`
- `tactical_execution_applied_count = 878`
- `tactical_execution_skipped_count = 1523`
- `unit_created_detected_count = 10`
- `army_presence_changed_count = 10`

Execution-layer boundary:

- legal tactical orders clearly occurred
- documented/planning state saw army presence
- execution-layer command application now occurs
- fallback execution source `self_units_combat_fallback` was exercised
- real applied execution reasons now include:
  - `army_rally_move_applied`
  - `defend_order_attack_applied`
  - `attack_order_command_applied`
- post-execution combat detection now also occurs with reason
  `execution_applied_with_enemy_contact`

## Checkpoint Decision

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = passed`
- `actual_game_time_sufficient = yes`
- `capability_validation_status = capability_validated_target`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = task_013_baseline_easy_pool_batch_evaluation`

## Interpretation

This checkpoint accepts that R3 is no longer diagnostic-only:

- at least one legal tactical order occurred in a valid real probe
- `own_army_count > 0` held during tactical planning
- tactical minimum therefore passes

This checkpoint accepts tactical target success at the queue gate level:

- post-execution combat detection now occurs
- `combat_event_detected_count = 13`
- execution-applied telemetry and contact-neighbor telemetry now align
- replay-backed corroboration is still pending, but it is treated here as a residual caveat rather than a blocking prerequisite for batch entry

The phase-level failure class is now:

- `none`

## What This Proves

- tactical minimum is accepted
- tactical minimum and target are both accepted for batch entry
- R3 no longer blocks entry into baseline batch

## What This Does Not Prove

- it does not provide a replay-reviewed combat narrative
- it does not prove target-level stability across a batch
- it does not allow planning counts alone to stand in for executed combat
