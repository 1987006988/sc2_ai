# R2 Army Presence Probe Report

Date: 2026-04-25
Task: `task_008_real_army_presence_probe`

## Run

- run dir: `data/logs/evaluation/r2_army_presence_probe/reallaunch-c59869c3`
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

Production / army-presence signals:

- `train_command_issued = 11`
- `combat_unit_production_success = 11`
- `queued_after_train = 11`
- `queued_after_train_zero_delta = 11`
- `unit_created_detected = 10`
- `unit_alive_after_short_window = 0`
- `army_presence_changed = 10`
- `max_own_army_count = 10`
- `attack_order_count = 334`

Observation-channel split:

- `max_documented_own_army_count = 10`
- `max_legacy_own_army_count = 0`
- `max_combat_unit_count = 0`

Interpretation:

- `combat_unit_production_success` is still command-level only
- queue-entry delta from `already_pending(...)` stayed zero for all observed train commands
- but `on_unit_created(...)` fired 10 times for zealots
- documented `own_army_count` rose to 10
- `attack_order` was emitted with `own_army_count = 10`
- the remaining discrepancy is in the legacy/classification channel, not in basic army materialization

## Replay Cross-Check

- replay artifact exists: `yes`
- automated replay parser available in this environment: `no`
- manual replay review performed in this turn: `no`
- replay-visible friendly combat unit summary: replay is saved, but this turn did not produce an independent replay-backed statement about friendly combat-unit appearance

## Failure Classification

Current best fit:

- `state_extraction_or_army_classification_failure`

Reasoning:

- `unit_created_detected > 0`
- `army_presence_changed > 0`
- `max_own_army_count > 0`
- `attack_order_count > 0`
- yet the legacy `bot_ai.army`-derived channel remained zero and `unit_alive_after_short_window` stayed zero because it still depends on that legacy observation path
- so the dominant discrepancy is no longer `true_production_path_failure`; it is now best explained as a state extraction / army classification issue in the legacy path

## Minimum Gate

`passed_with_replay_review_caveat`

Reason:

- valid real probe shows `own_army_count > 0`
- `on_unit_created(...)` confirms friendly combat-unit creation
- `army_presence_changed` confirms army-presence transitions
- replay artifact is present, but replay-backed corroboration was not completed in this turn

## Target Gate

`failed`

Reason:

- this is one rerun only
- replay-backed corroboration is still pending
- `unit_alive_after_short_window` did not validate through the legacy channel
- repeatability and fully clean rally/army-input confidence are not yet established

## Stretch Gate

`failed`

Reason:

- although attack orders appeared, the legacy survival/classification channel is still inconsistent
- this is not yet a clean tactical-stage input contract

## What This Proves

- this rerun is valid L3 evidence
- friendly combat units were created in the real match
- documented `own_army_count` rose above zero to 10
- the root problem has narrowed away from broad production failure and toward legacy state extraction / army classification mismatch

## What This Does Not Prove

- it does not complete replay-backed corroboration
- it does not prove target-level stability
- it does not justify skipping `checkpoint_C_army_core_gate`
- it does not prove the legacy army-count channel is safe to use without further repair
