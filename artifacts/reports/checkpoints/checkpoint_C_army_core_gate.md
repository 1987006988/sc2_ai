# checkpoint_C_army_core_gate

Date: 2026-04-25

## reviewed_tasks

- `task_007_rewrite_combat_unit_production_and_rally_logic`
- `task_008_real_army_presence_probe`

## minimum_gate_passed

`true`

Reason:

- valid real probe evidence exists for `task_008`
- `on_unit_created(...)` produced direct unit-creation evidence
- documented `own_army_count` rose above zero to `10`
- `army_presence_changed` also rose above zero in the same real probe

This minimum pass is established primarily on the documented channel, not on the
legacy `bot_ai.army` channel.

## target_gate_passed

`false`

Reason:

- replay-backed corroboration is still pending
- `unit_alive_after_short_window = 0`
- `max_legacy_own_army_count = 0`
- `max_combat_unit_count = 0`
- current evidence is sufficient to establish first-army minimum, but not
  enough to claim stable production-plus-rally confidence for tactical probing
  without caveat

## stretch_gate_status

`failed`

Reason:

- the army-observation split remains unresolved between documented and legacy
  channels
- current `attack_order` telemetry is still better interpreted as planning
  telemetry than as executed friendly-combat evidence

## actual_game_time_sufficient

`yes`

Reason:

- `max_game_time = 428.5714285714286`
- the reviewed claim is first-army existence / army-core minimum, not final
  tactical success

## capability_validation_status

`capability_validated_minimum`

For the army-core phase only.

## failure_class

`state_extraction_or_army_classification_failure`

## decision

`accepted_continue`

## next_allowed_task

- `task_010_rewrite_defend_attack_transition_logic`

## evidence_paths

- `artifacts/reports/r2_army_presence_probe/task_007_static_validation.md`
- `artifacts/reports/r2_army_presence_probe/report.md`
- `data/logs/evaluation/r2_army_presence_probe/summary.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match_result.json`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/telemetry/events.jsonl`
- `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3/match.SC2Replay`

## What This Proves

- the army-core minimum gate is now met on documented evidence
- first friendly combat-unit creation is real, not just command telemetry
- the dominant blocker has moved from broad production failure to legacy army
  visibility / classification mismatch
- the project may enter the next tactical-logic implementation step

## What This Does Not Prove

- it does not prove replay-backed corroboration
- it does not prove target-level stability
- it does not prove executed friendly combat
- it does not prove the legacy `bot_ai.army` path is reliable
- it does not let later phases treat planning telemetry as combat validation
