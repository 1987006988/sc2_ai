# Plan: Real Local Match Enablement

## Status

Completed

## Goal

Move the project from process-launch validation to a real map-driven local SC2
match entry using the approved phase-1 `python-sc2` base.

## Context

The local machine now has a confirmed SC2 installation root:

- `D:\games\StarCraft II`

The next smallest meaningful step is:

1. install a minimal ladder/bot-friendly map pack into the SC2 `Maps` root;
2. update project configs to point at real maps and a real built-in opponent;
3. upgrade `evaluation/runner/run_match.py` and `src/sc2bot/runtime/game_loop.py`
   so a real local match can be attempted through the project entrypoint.

## Constraints

- Do not change the approved route.
- Do not add research-side code into `src/sc2bot/`.
- Do not add strategy features.
- Keep evaluation responsible only for orchestration and result persistence.
- Keep replay summary / explanation out of scope.

## Scope

In:

- SC2 map installation and config updates;
- runtime preflight extension for real maps;
- real local match attempt path through evaluation;
- minimal tests and docs updates.

Out:

- stronger bot logic;
- SMAC, LLM, replay learning, or world-model work;
- long-running ladder evaluation.

## Done When

- `D:\games\StarCraft II\Maps` exists and contains at least one real ladder-test map;
- `configs/maps/local_test_maps.yaml` references real installed maps;
- `run_match.py` supports a real local match attempt path;
- failures persist to the result directory;
- docs and verification commands reflect the new capability.

## Verification Steps

- `python -m pytest tests/unit tests/integration`
- `scripts/setup/check_env.ps1`
- one real local match probe through `evaluation.runner.run_match`

## Risks

- local environment may still miss a stable python-sc2 runtime path;
- installed map names may not resolve the same way across wrappers;
- a real match can fail above the map layer but below the full bot loop.

## Recovery Notes

If another session resumes:

- read `AGENTS.md`
- read `docs/context/current_status.md`
- inspect `configs/maps/local_test_maps.yaml`
- inspect `evaluation/runner/run_match.py`
- inspect `src/sc2bot/runtime/game_loop.py`
