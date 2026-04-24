# AGENTS.md

## Project Goal

Build a layered hybrid full-game StarCraft II bot.

The current mainline objective is:

1. first reach an accepted playable baseline;
2. then validate a single adaptive research feature on top of that baseline.

The active execution authority is the current research control layer:

- `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/experiments/real_match_validation_protocol.md`
- `docs/experiments/checkpoint_acceptance_spec.md`
- `docs/plans/active/phase_playable_core_rebuild.md`
- `docs/plans/active/phase_adaptive_response_research.md`
- `docs/agents/codex_execution_rules_research_mode.md`

Old phase plans are historical references only.

## Current Scope

- Mainline bot code lives only in `src/sc2bot/`.
- Research prototypes live in `research/`.
- Evaluation orchestration lives in `evaluation/`.
- Runtime and evaluation configs live in `configs/`.
- Long-term project memory lives in `docs/`.

## Directory Navigation

- `src/sc2bot/`: production bot runtime, managers, config, telemetry, and
  stable interfaces.
- `research/`: prototypes, notebooks, ablations, SMAC, replay learning, LLM
  coach, combat predictor experiments.
- `evaluation/`: match runners, batch orchestration, metrics, reports.
- `configs/`: bot, map, opponent, evaluation, and logging configs.
- `data/`: replays, parsed data, features, logs. Large generated data should
  not be committed by default.
- `artifacts/`: generated models, reports, plots, checkpoints, replay artifacts.
- `docs/`: context, plans, handoffs, lessons, templates, commands, and control
  files.
- `scripts/`: repeatable setup, development, data, and docs commands.
- `tests/`: unit and integration tests for mainline infrastructure.

## Mainline / Research Boundary

- Do not import `research/` from `src/sc2bot/`.
- Do not place notebooks, SMAC experiments, LLM prompts, replay exploration, or
  one-off ablation scripts in `src/sc2bot/`.
- Prototype code must pass promotion rules before moving into `src/sc2bot/`.
- Evaluation code may run the bot, but bot decision logic must stay out of
  `evaluation/`.

## How to Run

Initial commands:

- Environment check: `scripts/setup/check_env.ps1`
- Unit tests: `python -m pytest tests/unit`

Validated real-match commands and variants should be read from:

- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`
- `docs/handoffs/latest.md`

## Validation Discipline

- `completed != validated`
- `diagnostic != capability`
- unit tests prove code logic only
- dry-runs prove orchestration only
- real matches are required for gameplay capability claims
- multi-match batches are required for stability claims
- checkpoint failure blocks progression

Never use historical completed tasks as proof that a capability is accepted.

## Planning Rules

Write or update a plan in `docs/plans/active/` before:

- changing multiple mainline modules;
- adding a manager;
- changing telemetry or data schema;
- adding an evaluation protocol;
- promoting prototype code;
- changing architecture boundaries;
- introducing a new external dependency;
- starting work expected to take more than half a day.

For current execution, the authoritative task source is:

- `docs/plans/active/research_master_task_queue.yaml`

Do not resume any legacy phase queue as if it were still active.

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
- Do not use LLMs as the real-time control layer.
- Do not put research scripts or notebooks into `src/sc2bot/`.
- Do not rely on chat history as project memory.
- Do not silently change architecture boundaries without plan updates.
- Do not treat historical phase plans as execution authority.
- Do not continue past a failed checkpoint.

## Before Finishing a Task

- Update the relevant control file or create a handoff.
- Record verification commands and results.
- Update `docs/context/current_status.md` if the control state changed.
- Add a lesson if a non-obvious failure or repeated pitfall was discovered.
- Keep `docs/handoffs/latest.md` aligned with the current active control layer.
