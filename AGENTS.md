# AGENTS.md

## Project Goal

Build a layered hybrid full-game StarCraft II bot.

Phase 1 focuses on:

- runnable full-game skeleton;
- local evaluation loop;
- minimal telemetry and logs;
- opponent modeling / hidden-state inference interface.

Phase 1's only primary research feature is opponent modeling / hidden-state inference.

## Current Scope

- Mainline bot code lives only in `src/sc2bot/`.
- Research prototypes live in `research/`.
- Evaluation orchestration lives in `evaluation/`.
- Runtime and evaluation configs live in `configs/`.
- Long-term project memory lives in `docs/`.

## Directory Navigation

- `src/sc2bot/`: production bot runtime, managers, config, telemetry, and stable interfaces.
- `research/`: prototypes, notebooks, ablations, SMAC, replay learning, LLM coach, combat predictor experiments.
- `evaluation/`: fixed opponent pools, batch matches, metrics, reports.
- `configs/`: bot, map, opponent, evaluation, and logging configs.
- `data/`: replays, parsed data, features, logs. Large generated data should not be committed by default.
- `artifacts/`: generated models, reports, plots, checkpoints, replay artifacts.
- `docs/`: context, ADRs, plans, handoffs, lessons, templates, commands.
- `scripts/`: repeatable setup, development, data, and docs commands.
- `tests/`: unit and integration tests for mainline infrastructure.

## Mainline / Research Boundary

- Do not import `research/` from `src/sc2bot/`.
- Do not place notebooks, SMAC experiments, LLM prompts, replay exploration, or one-off ablation scripts in `src/sc2bot/`.
- Prototype code must pass promotion rules before moving into `src/sc2bot/`.
- Evaluation code may run the bot, but bot decision logic must stay out of `evaluation/`.

## How to Run

Initial commands:

- Environment check: `scripts/setup/check_env.ps1`
- Local bot skeleton: `scripts/dev/run_bot_local.ps1`
- Smoke evaluation skeleton: `scripts/dev/run_smoke_eval.ps1`
- Unit tests: `python -m pytest tests/unit`

## Verification

Every mainline task must state:

- Goal
- Context
- Constraints
- Done when
- Verification steps

Use `docs/templates/task_template.md` for non-trivial tasks.

## Planning Rules

Write a plan in `docs/plans/active/` before:

- changing multiple mainline modules;
- adding a manager;
- changing telemetry or data schema;
- adding an evaluation protocol;
- promoting prototype code;
- changing architecture boundaries;
- introducing a new external dependency;
- starting work expected to take more than half a day.

## Prototype Promotion Rules

A prototype may enter `src/sc2bot/` only if:

- it has a documented goal and result;
- it has a proposed stable interface;
- it has repeatable verification;
- it has no notebook-only dependency;
- it has a plan or ADR approving promotion;
- it includes tests or evaluation steps;
- it uses configs rather than hard-coded experiment paths;
- it produces telemetry when it affects bot behavior.

## Do Not

- Do not make AlphaStar-like end-to-end RL the current mainline.
- Do not make SMAC / SMACv2 the full-game mainline.
- Do not use LLMs as the real-time control layer in phase 1.
- Do not put research scripts or notebooks into `src/sc2bot/`.
- Do not rely on chat history as project memory.
- Do not silently change architecture boundaries without ADR or plan updates.

## Showcase vs Mainline

- Structured strategy explanation and replay summary are showcase enhancements.
- They do not block phase-1 mainline completion.

## Before Finishing a Task

- Update the relevant plan or create a handoff.
- Record verification commands and results.
- Add or update an ADR if architecture changed.
- Add a lesson if a non-obvious failure or repeated pitfall was discovered.
- Keep `docs/context/current_status.md` accurate after milestone changes.
