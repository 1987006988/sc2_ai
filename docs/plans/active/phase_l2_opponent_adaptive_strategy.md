# Phase L2: Opponent-Adaptive Strategy

Status: planned.

## Goal

Make opponent modeling affect real strategy behavior, not only telemetry tags.

This phase builds on a playable core. It should compare behavior paths with and without opponent modeling.

## Scope

- `rush_risk` triggers defensive response or delayed attack.
- `low_information` increases scout persistence.
- macro/greedy signal can trigger a timing attack.
- `tech_risk` changes scouting priority or alert posture.
- Null vs opponent_model ablation over behavior metrics.
- Metrics for attack timing, defend posture, scout persistence, and strategy adaptation count.

## Non-goals

- No claim of win-rate improvement without evidence.
- No tag-only ablation as final proof.
- No complex full-strategy planner.
- No replay imitation learning integration.
- No SMAC or LLM control.
- No research code imports into `src/sc2bot/`.

## Files Likely To Change

- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/managers/scouting_manager.py`
- `src/sc2bot/managers/tactical_manager.py`
- `src/sc2bot/managers/micro_manager.py`
- `src/sc2bot/opponent_model/`
- `src/sc2bot/telemetry/`
- `configs/bot/`
- `configs/evaluation/`
- `evaluation/metrics/`
- `evaluation/reports/`
- tests under `tests/`

## Verification

- Run null vs opponent_model ablation on the same map/opponent pool.
- Include aggressive, macro, and tech-like opponent archetypes when available.
- Compare attack timing, defend posture, scout persistence, and adaptation count.
- Keep win-rate interpretation separate from behavior-path validation.

## Done Criteria

- Opponent model changes at least one real behavior path.
- Behavior differences are visible in telemetry and replay.
- Metrics distinguish tag-only responses from actual behavior changes.
- Report clearly states what improved, what did not, and what remains unproven.

## Stop Conditions

- If the playable core is not stable, stop and return to Phase L1.
- If behavior changes are only telemetry tags, do not mark Phase L2 complete.
- If archetype opponent setup is missing, stop and create a focused evaluation setup task.
