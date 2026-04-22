# Phase B: Playable Competitive Core

Status: not accepted. Original task queue exhausted, but objective not accepted.
Superseded for revalidation by
`docs/plans/active/phase_b_revalidation_playable_core.md`.

Task queue: `docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml`

Manual trigger: `docs/plans/active/phase_b_manual_trigger.md`

## Goal

Make the Protoss bot a playable baseline that can build, produce combat units, defend, attack, and run against defined baseline opponents.

This is the first phase where real gameplay behavior, replay quality, build progression, combat-unit production, army orders, and combat telemetry become core acceptance criteria. It does not claim ladder competitiveness.

## Scope

- probe production;
- pylon;
- gateway;
- assimilator;
- cybernetics core;
- zealot/stalker production;
- army rally;
- defend own base;
- attack known enemy base;
- basic retreat/regroup if it stays minimal;
- combat telemetry.

## Non-goals

- No full advanced build-order optimizer.
- No expansion strategy unless separately approved.
- No full tech-tree strategy.
- No upgrades.
- No advanced tech beyond the minimum Cybernetics Core path.
- No complex army composition.
- No SMAC, LLM, replay learning, learned opponent model, combat predictor, or league/self-play work.
- No learned micro module in the mainline.
- No opponent-adaptive claims before Phase C.
- No ladder competitiveness claim.
- No opponent-model win-rate claim.

## Files Likely To Change

- `src/sc2bot/managers/macro_manager.py`
- `src/sc2bot/managers/tactical_manager.py`
- `src/sc2bot/managers/micro_manager.py`
- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/domain/decisions.py`
- `src/sc2bot/runtime/game_loop.py`
- `configs/bot/`
- `evaluation/metrics/`
- `evaluation/reports/`
- tests under `tests/`

## Verification

- Unit tests for build and combat decision logic.
- Real matches against built-in Easy and Medium opponents.
- Multi-match evaluation report with win/loss, build completion, combat, and crash/timeout metrics.
- Replay inspection for build progression and attack/defend behavior.

## Real-Match-First Rules

1. Unit tests only prove code logic.
2. Dry-run only proves orchestration flow.
3. Real matches are required to prove gameplay behavior.
4. Every gameplay feature needs a real SC2 probe before it can be treated as validated.
5. Multi-match batches are required to prove stability.
6. Dry-run and unit-test evidence must not be framed as real capability evidence.
7. Every L3 task must record evidence paths.
8. Every task must fit one Plus 5-hour quota window; if scope expands, mark `split_required`.

## Done Criteria

- The bot repeatedly completes basic Protoss build progression when not disrupted.
- The bot produces zealots and/or stalkers.
- The bot defends own base and attacks known enemy base.
- Combat telemetry records engagements, units killed/lost where available, and defend/attack commands.
- The bot has measured outcomes against built-in Easy/Medium, without overclaiming beyond the data.

## Closeout Gate

Phase B cannot close unless:

- Gateway real probe completes at L3.
- Assimilator/Cybernetics Core real probe completes at L3.
- Combat-unit production real probe completes at L3.
- Attack/defend order real probe completes at L3.
- Combat event real probe completes at L3, or records a clear structured reason for no combat.
- Phase B small real evaluation completes at L3.
- Phase B report uses real match data.
- Report states whether the current bot beats built-in Easy/Medium in the collected data.
- Report does not claim ladder competitiveness.

## Evidence Audit Reclassification

Audit path: `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`

Original Phase B state after audit:

- task queue exhausted;
- objective not accepted;
- playable baseline not reached;
- Level 1 not reached;
- Phase C blocked.

The 2026-04-22 audit separates task execution, diagnostic evidence, and gameplay
capability validation. Phase B task completion must not be read as capability
acceptance.

The audited real probes and the 8-match small eval all ended around
`game_time=116.07` with `status=max_game_time_reached`. The primary cutoff was
the bot runtime self-exit from `src/sc2bot/runtime/game_loop.py`, controlled by
`configs/bot/debug.yaml` with `runtime.max_game_loop: 2600`.

Current reclassification:

- Gateway command telemetry is partially validated: `gateway_build_attempt` and
  `gateway_build_success` appeared in real telemetry.
- Gateway-ready, Assimilator/Cyber Core, combat-unit production, real army
  attack/defend orders, and friendly combat are not validated because the match
  window ended before their minimum opportunity windows.
- Phase B small eval is valid as multi-match diagnostic evidence, but not as
  playable-baseline capability evidence.
- Phase B is not accepted as a playable competitive core and should not enter
  Phase C yet.

Recommended order:

1. Fix or parameterize the Phase B real-match duration window.
2. Rerun Gateway-ready, Cyber Core, and combat-unit production probes.
3. Rerun attack/defend and combat probes only after real friendly army units
   exist.
4. Regenerate the Phase B small eval and report before reconsidering closeout.

## Stop Conditions

- If building placement becomes unstable, split placement into a dedicated task.
- If production logic causes runtime crashes, stop and stabilize production before adding combat.
- If win/loss metrics are noisy, increase repeat count or report uncertainty rather than overclaiming.
