# Phase 1 Scope

## Phase 1 Goal

Deliver a single-race, fixed-map-pool, layered hybrid full-game SC2 bot skeleton with:

- a local evaluation loop;
- telemetry and replay metadata;
- an opponent model interface and minimal implementation;
- a fixed-opponent-pool validation path.

## In Scope

- Mainline repository skeleton and stable module boundaries.
- Runtime, managers, config loading, and telemetry stubs.
- Evaluation skeleton and fixed local opponent pool config.
- Single-race bot setup.
- Fixed map pool configuration.
- Rule-based or null opponent model baseline.
- Telemetry and replay metadata sufficient for phase-1 validation.
- Research prototype space for opponent modeling, replay learning, SMAC, LLM coach, and combat prediction.

## Out of Scope

- End-to-end RL training.
- Full replay imitation pipeline in production.
- SMAC runtime integration into the bot.
- LLM-driven real-time control.
- Full world-model planning.
- Large-scale offline RL training.

## Mainline

- `src/sc2bot/`

## Support and Side Lines

- Data line: `research/replay_learning/`
- Micro benchmark line: `research/smac_micro/`
- LLM coach line: `research/llm_coach/`
- Optional phase-2 exploration: `research/combat_predictor/`

## Unique Phase 1 Research Feature

- Opponent modeling / hidden-state inference.

No second primary research feature should compete with this in phase 1.

## Phase 1 Validation Requirement

Phase 1 is not complete without a fixed-opponent-pool ablation:

- without opponent model;
- with opponent model.

This is the minimum research validation requirement.

## Showcase Enhancements

These are allowed in phase 1, but they are not blocking mainline completion:

- structured strategy explanation;
- replay summary.

## Success Criteria

- Bot skeleton starts and executes a dry-run flow.
- Smoke evaluation config loads and runs through the evaluation skeleton.
- Telemetry writes stable event records.
- Opponent model interface exists and supports null and rule-based implementations.
- A fixed opponent pool exists for validation.
- A with/without opponent model ablation protocol is defined.
