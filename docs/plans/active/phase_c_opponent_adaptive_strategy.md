# Phase C: Opponent-Adaptive Strategy

Status: planned.

## Goal

Make opponent modeling / hidden-state inference change actual behavior paths in real matches.

This phase depends on Phase B providing a playable core. Telemetry tags alone are not enough.

## Scope

- `rush_risk` changes defensive response or delays attack.
- `low_information` extends scouting.
- macro/expansion signal can trigger a timing attack.
- `tech_risk` changes scouting priority or alert posture.
- null vs opponent_model behavior ablation.
- behavior metrics for attack timing, defend posture, scout persistence, and strategy adaptation count.

## Non-goals

- No claim that opponent modeling improves win rate unless repeated real data supports it.
- No tag-only ablation as completion evidence.
- No full learned opponent model unless promoted through Phase E.
- No research imports into `src/sc2bot/`.
- No SMAC/LLM/world-model control path.

## Files Likely To Change

- `src/sc2bot/opponent_model/`
- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/managers/scouting_manager.py`
- `src/sc2bot/managers/tactical_manager.py`
- `src/sc2bot/managers/micro_manager.py`
- `src/sc2bot/telemetry/`
- `configs/bot/`
- `configs/evaluation/`
- `evaluation/metrics/`
- `evaluation/reports/`
- tests under `tests/`

## Verification

- Real null vs opponent_model ablation on identical map/opponent/config pools.
- Behavior-level metrics, not only telemetry tags.
- Separate behavior conclusions from win/loss conclusions.
- Evidence paths for all real match outputs.

## Done Criteria

- Opponent model changes at least one actual behavior path in real matches.
- Reports quantify attack timing, defend posture, scout persistence, and strategy adaptation count.
- Win/loss metrics are included but not overstated.
- The report distinguishes observation signals, prediction signals, selected responses, and behavior changes.

## Stop Conditions

- If Phase B playable core is unstable, stop and return to Phase B.
- If behavior changes are only telemetry tags, do not mark Phase C complete.
- If opponent archetypes are unavailable, split out an opponent-pool setup task.
