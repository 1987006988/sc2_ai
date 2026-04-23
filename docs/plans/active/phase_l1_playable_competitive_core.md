# Phase L1: Playable Competitive Core

Status: legacy_historical_reference
Execution authority: no
Superseded by: `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`

Legacy note: retained as historical phase planning context only. It must not be
used as the current execution authority.

## Goal

Give the Protoss bot a minimal but real gameplay core that can produce a visible build progression, combat units, attack/defend behavior, and combat telemetry.

This is the first phase where replay quality matters. The goal is basic playable competence, not high win rate.

## Scope

- Single-race Protoss core.
- Stable opening.
- Probe production and supply sustain.
- Gateway placement.
- Assimilator placement.
- Cybernetics Core placement.
- Zealot/Stalker production.
- Army rally.
- Defend own base.
- Attack known enemy base.
- Basic retreat/regroup.
- Combat telemetry.

## Non-goals

- No advanced build-order optimizer.
- No expansion plan unless separately approved.
- No full tech tree.
- No complex tactical AI.
- No learned micro in this phase.
- No claim of strong ladder performance.

## Files Likely To Change

- `src/sc2bot/managers/macro_manager.py`
- `src/sc2bot/managers/tactical_manager.py`
- `src/sc2bot/managers/micro_manager.py`
- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/runtime/game_loop.py`
- `src/sc2bot/domain/decisions.py`
- `configs/bot/`
- `evaluation/metrics/`
- tests under `tests/`

## Verification

- Real local matches against built-in Easy and Medium opponents.
- Replay inspection confirms build progression and combat units.
- Telemetry includes build, army, attack, defend, and combat events.
- Evaluation summary includes build completion, first attack time, combat count, and game duration.

## Done Criteria

- Replay shows probe/pylon/gateway/assimilator/cyber core progression when resources and conditions allow.
- Replay shows zealot or stalker production.
- Replay shows defend or attack behavior.
- Telemetry records combat events.
- Repeated built-in opponent evaluation is possible without elevated crash rate.

## Stop Conditions

- If placement logic becomes brittle, split building placement into its own task.
- If army behavior destabilizes runtime, fall back to rally/defend only and document the blocker.
- If a build-order implementation grows beyond minimal scope, stop and split planning.
