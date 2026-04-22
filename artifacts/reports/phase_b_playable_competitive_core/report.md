# Phase B Playable Competitive Core Report

Generated: 2026-04-22 21:40 +08:00

Source run: `phase_b_small_eval_20260422`

Source data:

- `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/summary.json`
- `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/phase_b_small_eval_metrics.json`

## Scope

This report summarizes real SC2 local match evidence from `task_13_phase_b_small_eval`.

It uses real match output only. It does not use unit tests or dry-run data as gameplay evidence.

## Evaluation Setup

- Matches: 8
- Map: `incorporeal_aie_v4`
- Bot config: `configs/bot/debug.yaml`
- Opponents:
  - `builtin_easy_terran`: 2 matches
  - `builtin_easy_zerg`: 2 matches
  - `builtin_easy_protoss`: 2 matches
  - `builtin_medium_terran`: 2 matches

## Artifact Completeness

- Missing `match_result.json`: 0
- Missing replay: 0
- Missing telemetry: 0
- Crash count: 0
- Timeout count: 0

All 8 matches persisted result, replay, and telemetry artifacts.

## Status And Results

- `max_game_time_reached`: 8
- `Result.Defeat`: 8

This data does not show wins against built-in Easy or Medium opponents.

## Build Progression Metrics

- Gateway build success count: 8
- Combat-unit production success count: 0
- Telemetry events with `own_army_count > 0`: 0

Interpretation: Gateway command progression is visible in real matches, but Phase B has not yet produced a real friendly army in the evaluated window.

## Army Order Metrics

- Army-order events: 5208
- `defend_order` count: 3388
- `attack_order` count: 0

Interpretation: The tactical layer records real-match defensive posture when enemies are visible, but there is no evidence of real attack-order behavior in this evaluation.

## Combat Telemetry Metrics

- `combat_event_detected`: 3388
- `enemy_combat_unit_nearby`: 3388
- `own_army_positive_event_count`: 0

Interpretation: Combat telemetry is currently enemy-contact signal telemetry. It is not evidence of friendly combat execution, kills, losses, or effective micro.

## Level 1 Assessment

Level 1 playable baseline bot is not reached.

Reasons:

- No combat-unit production succeeded in the 8-match real evaluation.
- No telemetry event reported `own_army_count > 0`.
- No `attack_order` appeared.
- All matches ended as `Result.Defeat`.

## What This Proves

- The bot can run an 8-match real local small evaluation against built-in Easy/Medium opponents.
- Every match persisted result, replay, and telemetry artifacts.
- Gateway build commands were issued successfully in every match.
- Army-order and combat-signal telemetry are present in real match output.
- Crash, timeout, and missing-artifact accounting works for this small eval.

## What This Does Not Prove

- It does not prove combat-unit production in real gameplay.
- It does not prove attack orders with friendly army units.
- It does not prove wins against built-in Easy or Medium.
- It does not prove gameplay quality.
- It does not prove ladder competitiveness.
- It does not prove opponent modeling improves match outcomes.

## Known Limitations

- The current short runtime window reaches Gateway command issuance but not a playable army.
- Combat-unit production remains at zero in this real evaluation.
- Combat events are primarily enemy-visible signals.
- The report is a small Phase B evaluation, not a ladder benchmark.

## Recommended Next Step

Before claiming Phase B as a playable competitive core, add a focused task to make real combat-unit production happen within the evaluation window, then rerun the real production and attack/defend probes.
