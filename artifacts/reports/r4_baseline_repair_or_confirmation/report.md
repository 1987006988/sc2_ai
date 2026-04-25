# R4 Baseline Repair Or Confirmation Report

Date: 2026-04-25
Task: `task_014_baseline_repair_or_confirmation`

## Repair Scope

Focused repair applied:

- dominant failure class from `task_013` was treated as sustained production / spending weakness
- scope was kept to a single baseline production-capacity change
- baseline now targets `2` Gateways instead of `1`

Files carrying the repair:

- `src/sc2bot/config/schema.py`
- `src/sc2bot/runtime/game_loop.py`
- `configs/bot/baseline_playable.yaml`

No adaptive logic was introduced.
No broader opponent slice was added.

## Focused Rerun Design

- config: `configs/evaluation/r4_baseline_repair_or_confirmation.yaml`
- map slice: `IncorporealAIE_v4`
- opponent slice: `builtin_easy_terran`
- repeats: `2`
- intent: test the exact outcome-level weakness identified by `task_013` without expanding scope

## Outcome Summary

- total rerun matches: `2`
- wins: `2`
- defeats: `0`

Match roots:

- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e`

## Improvement Against Task 013 Failure Class

Reference from the valid Terran slice inside `task_013`:

- outcome: `0/2` wins
- `gateway_build_success = 1` per run
- `combat_unit_production_success = 11` per run
- `unit_created_detected = 10` per run
- `max_own_army_count = 8-9`
- end minerals about `3460-3525`

Focused rerun after repair:

- outcome: `2/2` wins
- `gateway_build_success = 2` per run
- `combat_unit_production_success = 17-19`
- `unit_created_detected = 15-17`
- `max_own_army_count = 12-15`
- end minerals about `2210-2235`

## Interpretation

This focused rerun shows a direct improvement on the dominant failure class from
`task_013`:

- production capacity increased in the repaired slice
- combat-unit creation increased materially
- peak army size increased materially
- floating minerals decreased materially
- outcome changed from repeated defeat to repeated victory on the rerun slice

This does **not** prove Level 1 acceptance by itself. That decision still
belongs to `checkpoint_E_level1_baseline_gate`.

But it **does** show that the highest-priority R4 repair was both focused and
effective.

## Failure Classification

Current best fit:

- `none` for this focused rerun

Reasoning:

- the specific dominant failure class from `task_013` was targeted directly
- the rerun improved the intended gameplay chain and outcome together
- no new prerequisite regression was observed in the focused slice

## Minimum Gate

`passed`

Reason:

- the focused rerun clearly improved the dominant failure class from `task_013`
- the improvement is not only telemetry-level; it also changed outcome to `2/2` wins

## Target Gate

`passed`

Reason:

- the repair gives `checkpoint_E` enough evidence to decide baseline acceptance
  without asking for another large-scope repair before review

## Stretch Gate

`pending_checkpoint_review`

Reason:

- this focused Terran rerun is strong evidence
- but the claim that baseline is fully frozen and ready as adaptive control
  should still be made at `checkpoint_E`, not inside this repair task alone

## What This Proves

- a single-scope repair can materially improve the dominant R4 failure class
- the baseline can now win at least a focused easy-Terran rerun slice
- the production-capacity bottleneck identified in `task_013` was real and actionable

## What This Does Not Prove

- it does not by itself prove full easy-slice repeated wins across all races
- it does not by itself prove Level 1 acceptance
- it does not justify skipping `checkpoint_E_level1_baseline_gate`

## Evidence Paths

- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/match.SC2Replay`
