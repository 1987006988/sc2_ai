# Phase E: Learning-Augmented Research Modules

Status: planned.

## Goal

Increase research depth through learning-augmented modules after the bot has a real match dataset and playable competitive core.

These modules are not blockers for Phases A/B/C, but the architecture should preserve clean interfaces for them.

## Candidate Branches

- replay/log imitation for build timing;
- learned opponent model;
- combat predictor;
- micro-control support branch via SMAC/custom scenarios.

## Scope

- use real match datasets and replays produced by earlier phases;
- keep research prototypes in `research/` until promotion criteria are met;
- promote only stable interfaces into `src/sc2bot/`;
- evaluate each module against a clear baseline.

## Non-goals

- No AlphaStar-like full end-to-end RL mainline.
- No SMAC policy directly controlling the full-game bot.
- No LLM real-time control.
- No notebook-only dependency in production.
- No research code import from `src/sc2bot/`.

## Files Likely To Change

- `research/`
- `data/`
- `evaluation/metrics/`
- `evaluation/reports/`
- promotion candidates under `src/sc2bot/` only after approval
- `docs/plans/`
- `docs/adr/` if architecture changes

## Verification

- Offline metrics for the research module.
- Real match or controlled scenario validation when the module affects gameplay.
- Ablation against the previous baseline.
- Clear evidence paths and reproducible commands.

## Done Criteria

- At least one learning-augmented module demonstrates value against a baseline.
- Any promoted interface has tests, configs, telemetry, and documented rollback.
- Reports separate offline validation, controlled-scenario validation, and real-match validation.

## Stop Conditions

- If the module lacks data quality, return to dataset collection.
- If the module cannot be evaluated against a baseline, do not promote it.
- If promotion would blur research/mainline boundaries, stop and write an ADR.
