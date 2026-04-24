# checkpoint_D_tactical_core_gate

Date: 2026-04-25

## reviewed_tasks

- `task_010_rewrite_defend_attack_transition_logic`
- `task_011_real_tactical_probe`

## minimum_gate_passed

`true`

Reason:

- a valid real probe exists
- at least one legal tactical order occurred with `own_army_count > 0`
- `defend_order` and `attack_order` both appeared in real-match telemetry
- the checkpoint does not rely on fake-army evidence to establish this minimum

## target_gate_passed

`false`

Reason:

- `friendly combat` was not validated
- `combat_event_detected_count = 0`
- the last combat-event payload remained
  `planning_signal_without_execution_evidence`
- replay-backed corroboration is still pending

## stretch_gate_status

`failed`

Reason:

- current evidence does not yet support a fair baseline batch entry
- planning telemetry is cleaner, but still not enough to establish executed
  friendly-combat evidence or a replay-backed near-contact narrative

## actual_game_time_sufficient

`yes`

Reason:

- the reviewed tactical probe reached a fair opportunity window
- the failure is not duration-related

## capability_validation_status

`capability_validated_minimum`

For the tactical phase only.

## failure_class

`logic_failure`

## decision

`repair_and_rerun`

## next_allowed_task

- `task_010_rewrite_defend_attack_transition_logic`

## evidence_paths

- `artifacts/reports/r3_tactical_probe/task_010_static_validation.md`
- `artifacts/reports/r3_tactical_probe/report.md`
- `data/logs/evaluation/r3_tactical_probe/summary.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-bb2aed30/match_result.json`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-bb2aed30/telemetry/events.jsonl`
- `data/logs/evaluation/r3_tactical_probe/reallaunch-bb2aed30/match.SC2Replay`

## What This Proves

- tactical-order minimum is no longer diagnostic-only
- legal `defend_order` / `attack_order` can occur in a real match with
  `own_army_count > 0`
- the dominant remaining gap is tactical execution / combat-evidence
  materialization, not army existence

## What This Does Not Prove

- it does not prove friendly combat
- it does not prove replay-backed contact
- it does not justify entering baseline batch evaluation yet
- it does not allow planning telemetry to be treated as executed-combat evidence
