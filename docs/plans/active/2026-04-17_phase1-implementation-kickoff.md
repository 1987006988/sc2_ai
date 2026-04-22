# Plan: Phase 1 Implementation Kickoff

## Status

Completed

## Goal

Start phase-1 implementation by:

1. validating and selecting the first engineering base between Ares-sc2 and bare python-sc2;
2. upgrading evaluation from config-loading only to a minimal local match orchestration loop with result persistence;
3. creating the first opponent-modeling prototype package and ablation protocol in `research/opponent_modeling/`.

## Context

The technical route is formally approved. The next priority is execution, not more route discussion. Mainline must remain clean, and research code must stay outside `src/sc2bot/`.

Relevant files:

- `AGENTS.md`
- `docs/foundation/03_direction/direction_summary.md`
- `docs/foundation/03_direction/phase1_scope.md`
- `docs/context/current_status.md`

## Constraints

- Do not mix research code into `src/sc2bot/`.
- Do not implement large strategy logic yet.
- Do not introduce LLM runtime control or SMAC runtime integration.
- Keep evaluation orchestration outside the bot mainline.

## Scope

In:

- framework validation;
- ADR update or new ADR for framework choice;
- evaluation runner, result persistence, and opponent-pool config tightening;
- research/opponent_modeling README, interface notes, and ablation protocol draft.

Out:

- advanced macro logic;
- replay summary implementation;
- full replay-learning pipeline;
- combat predictor;
- SMAC training code.

## Proposed Changes

- validate available packages and runtime path;
- update configs and evaluation runners;
- persist match result and metadata;
- add research prototype docs and protocol;
- update ADR/context/handoff with results.

## Done When

- one engineering base is selected for phase 1;
- local smoke evaluation produces a saved match result and telemetry metadata;
- opponent-modeling prototype docs and ablation protocol exist under `research/opponent_modeling/`.

## Verification Steps

- `python -m pytest tests/unit tests/integration`
- `scripts/dev/run_bot_local.ps1`
- `scripts/dev/run_smoke_eval.ps1`
- framework import / startup validation commands

## Risks

- SC2 runtime or package dependencies may be unavailable locally;
- package choice may be constrained by environment rather than preference;
- evaluation loop may need a temporary mock adapter before real SC2 launch is available.

## Recovery Notes

If another session resumes this task:

- Read `AGENTS.md`
- Read this plan
- Read `docs/context/current_status.md`
- Inspect `evaluation/runner/`
- Inspect `research/opponent_modeling/`
