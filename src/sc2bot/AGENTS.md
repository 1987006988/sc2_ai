# src/sc2bot AGENTS.md

This directory is the production full-game bot mainline.

## Rules

- Keep runtime code stable and minimal.
- Do not import from `research/`.
- Do not embed evaluation orchestration here.
- Do not hard-code experiment paths or one-off parameters.
- Use `configs/` and typed schema objects for runtime settings.
- Record behavior-affecting decisions through telemetry.
- Prefer interfaces and stubs over premature algorithm complexity.

## Phase 1 Mainline Modules

- runtime skeleton;
- macro manager minimal flow;
- scouting manager minimal observations;
- strategy manager minimal decisions;
- tactical and micro manager stubs;
- opponent model interface with null and rule-based implementations;
- telemetry event logger;
- config loader.

## Done Standard

Mainline changes should include tests or a smoke command listed in `docs/commands/verification_matrix.md`.
