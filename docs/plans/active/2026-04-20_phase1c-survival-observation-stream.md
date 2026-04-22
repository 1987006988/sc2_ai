# Plan: Phase 1C Survival And Live Observation Stream

## Status

Completed

## Goal

Upgrade the current real-match skeleton into a minimal survival baseline that
stays alive for a bounded runtime and records live opponent-observation inputs
for later opponent-model ablation.

## Context

The project can now launch Windows StarCraft II from WSL through Windows Python,
run a real local match on installed AI Arena maps, and persist telemetry,
match results, replay metadata, and replay files.

## Constraints

- Keep mainline code in `src/sc2bot/`.
- Do not import `research/` from mainline code.
- Keep evaluation orchestration out of bot decision logic.
- Do not add SMAC, LLM, world-model, replay-learning, or complex strategy code.
- Prioritize stable live observation and bounded survival over win rate.

## Scope

In:

- enriched `GameState` and `ScoutingObservation` telemetry;
- minimal runtime survival actions and structured exit reasons;
- small built-in local opponent pool;
- opponent-model mode telemetry for later ablation.

Out:

- build-order systems;
- learned policies;
- replay parsing;
- showcase/replay-summary features.

## Done When

- real local match telemetry includes enriched game-state and scouting fields;
- the bot exits by configured max step/game-loop reason or records gameplay errors;
- a small built-in opponent pool can be batch-run;
- docs and verification commands record the validated path.

## Verification Steps

- `python -m pytest tests`
- one Windows real local match through `evaluation.runner.run_match`
- one small Windows real batch with at least two built-in opponents
- telemetry inspection for game-state, scouting, and opponent-model mode fields
