# Ladder-Competitive Adaptive SC2 Bot Plan

Status: active roadmap as of 2026-04-22.

Supersedes / integrates:

- `docs/plans/active/ladder_ready_adaptive_sc2_bot_roadmap.md`
- the paused Phase 1F demo-packaging direction
- any standalone Phase L0 execution direction that treats ladder readiness as the final goal

## Goal

Build a single-race Protoss layered hybrid StarCraft II bot that can:

- run repeated real bot-vs-bot matches in AI Arena / local-play-bootstrap / ladder-like environments;
- beat a defined set of baseline opponents;
- validate ability from real match data;
- use opponent modeling / hidden-state inference as the core research feature;
- leave stable interfaces for replay/log imitation, learned opponent models, combat predictors, and micro modules.

This is not a telemetry demo, not a "complete one game" demo, and not a simple script bot. The project goal is a real ladder-competitive bot with measurable gameplay capability.

## Existing Foundation

Phase 1D and Phase 1E are foundation milestones.

They prove:

- real SC2 runtime;
- telemetry persistence;
- opponent prediction;
- strategy response telemetry;
- report generation;
- L3 validation mechanics.

They do not prove:

- ladder competitiveness;
- stable win rate;
- gameplay quality improvement;
- opponent model improves match outcomes.

## Workload Principle

The project is not limited to a single 5-hour window.

Only each smallest Codex task should be quota-safe:

- one task should fit within one Plus 5-hour quota window;
- one task should have one small goal;
- one task must be verifiable;
- real ability claims require real SC2 evidence;
- every real match task must output evidence paths;
- if scope expands, stop and split the task.

## Real-Match-First Rules

- Unit tests only prove code logic.
- Dry-run only proves orchestration flow.
- A real match is required to prove gameplay behavior.
- Multi-match batch runs are required to prove stability.
- Opponent-pool evaluation is required for meaningful showcase value.
- Reports must separate synthetic, dry-run, single real match, and multi-match evidence.
- Dry-run conclusions must not be packaged as real capability claims.

## Target Levels

### Level 0: Real Match Data Foundation

The bot can run real matches repeatedly and persist replay/result/telemetry with dataset manifests and artifact checks.

### Level 1: Playable Baseline Bot, Beats Built-in Easy

The bot has a basic Protoss gameplay core and can repeatedly beat at least built-in Easy in controlled evaluation.

### Level 2: Competitive vs Built-in Medium

The bot has enough macro, combat production, defense, attack, and stability to compete against built-in Medium.

### Level 3: Opponent-Adaptive Behavior Validated

Opponent modeling changes actual behavior paths such as scouting persistence, defensive posture, attack timing, or retreat/regroup logic.

### Level 4: AI Arena / Local Opponent Pool Evaluation

The bot is evaluated against a broader local ladder-like opponent pool with crash/timeout/win-rate/gameplay metrics.

### Level 5: Learning-Augmented Research Modules

Replay/log imitation, learned opponent modeling, combat prediction, or micro modules improve or extend the bot through controlled experiments.

Interview showcase target: at least Level 3, ideally Level 4.

## Phases

### Phase A: Ladder Infrastructure & Real Match Dataset

Goal: establish the real ladder-like match and data-collection base.

Outputs:

- real match dataset;
- dataset manifest;
- baseline infrastructure report;
- crash/timeout/missing artifact statistics.

### Phase B: Playable Competitive Core

Goal: make the bot actually play a basic Protoss game and beat baseline opponents.

Outputs:

- built-in Easy / Medium evaluation report;
- build completion metrics;
- combat metrics;
- win/loss metrics.

### Phase C: Opponent-Adaptive Strategy

Goal: make opponent modeling change real strategy behavior.

Outputs:

- behavior-level ablation report;
- attack timing / defend posture / scout persistence metrics;
- strategy adaptation count;
- win/loss tracked separately from behavior conclusions.

### Phase D: Ladder Opponent Pool Evaluation

Goal: evaluate against a broader local ladder-like opponent pool.

Outputs:

- opponent pool evaluation matrix;
- crash/timeout/win-rate/gameplay metrics.

### Phase E: Learning-Augmented Research Modules

Goal: increase research depth through learning-augmented modules.

Outputs depend on selected branch:

- replay/log imitation for build timing;
- learned opponent model;
- combat predictor;
- micro-control support branch.

## Execution Rules

- Create quota-safe task queues per phase before implementation.
- Do not execute multiple phase tasks in one Codex turn.
- Do not claim a target level until its real evidence exists.
- Do not use synthetic or dry-run evidence for gameplay ability claims.
- Keep bot decision logic in `src/sc2bot/`.
- Keep evaluation orchestration in `evaluation/`.
- Do not import `research/` into `src/sc2bot/`.

## Next Recommended Step

Create a quota-safe task queue for Phase A: Ladder Infrastructure & Real Match Dataset.
