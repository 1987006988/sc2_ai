# Ladder-Ready Adaptive SC2 Bot Roadmap

Status: superseded / integrated on 2026-04-22.

Superseded by: `docs/plans/active/ladder_competitive_adaptive_sc2_bot_plan.md`

Reason: ladder readiness is necessary but too low as the project goal. The active target is now a ladder-competitive adaptive Protoss bot that can beat defined baseline opponents and validate ability through repeated real bot-vs-bot matches.

This roadmap supersedes the previous Interview Demo V0 packaging route as the active execution direction. Phase 1F demo packaging is paused until the bot has a ladder-ready playable core.

## Goal

Build a single-race layered hybrid full-game StarCraft II AI that can run in ladder-like bot-vs-bot matches and support real capability validation.

The goal is not to reproduce AlphaStar, to make SMAC the full-game mainline, or to stop at telemetry/reporting demos. The goal is a practical bot that combines:

- rule-based macro and procedural planning;
- learning-augmented tactical evaluation;
- learning-augmented micro modules;
- replay/log imitation for build timing and behavior priors;
- opponent modeling / hidden-state inference as the Phase 1 research feature.

## Phase 1D / 1E Repositioning

Phase 1D and Phase 1E are foundation milestones, not the final demo.

They prove:

- real SC2 local runtime;
- replay, result, telemetry, and report persistence;
- live GameState and ScoutingObservation flow;
- opponent prediction telemetry;
- StrategyManager response telemetry;
- minimal_behavior telemetry entry points;
- L3 real telemetry validation process.

They do not prove:

- the bot is ladder-ready;
- the bot has stable win rate;
- gameplay quality improved;
- opponent modeling improves real match outcomes;
- the current replay is strong enough for a final interview demo.

## Phase 1F Status

Phase 1F demo packaging is paused.

Reason: the current bot has validated runtime, telemetry, prediction, response, and reporting infrastructure, but it still lacks a playable competitive core. Packaging the current replay/report as a final demo would overstate the project. Demo packaging should resume only after ladder readiness and basic competitive gameplay are validated.

## Milestones

### Phase L0: Ladder Readiness

Goal: make the bot usable in ladder-like local evaluation and package checks.

Required capabilities:

- AI Arena/local-play compatible entrypoint;
- upload/package dry-run;
- map and opponent configuration;
- multi-match stability;
- crash and timeout handling;
- replay/result/telemetry persistence;
- fixed evaluation command.

Acceptance:

- local ladder-like runner can run multiple consecutive matches;
- package structure is checked;
- crash rate and timeout rate are reported;
- strength is not required.

### Phase L1: Playable Competitive Core

Goal: make the bot visibly play a basic Protoss game.

Required capabilities:

- single race Protoss;
- stable opening;
- probe, pylon, gateway, assimilator, cybernetics core;
- zealot/stalker production;
- army rally;
- defend own base;
- attack known enemy base;
- basic retreat/regroup;
- combat telemetry.

Acceptance:

- real replay shows build progression;
- real replay shows combat units;
- real replay shows attack/defend behavior;
- telemetry contains combat events;
- repeated evaluation vs built-in Easy/Medium is possible.

### Phase L2: Opponent-Adaptive Strategy

Goal: make opponent modeling alter real behavior paths, not only telemetry tags.

Required capabilities:

- rush_risk changes defensive response or delays attack;
- low_information extends scouting;
- macro signal can trigger timing attack;
- tech_risk changes scouting priority or alert posture;
- with/without opponent model ablation compares actual behavior metrics.

Acceptance:

- null vs opponent_model behavior paths differ;
- attack timing, defend posture, and scout persistence can be measured;
- aggressive, macro, and tech archetype opponents produce different adaptation metrics;
- conclusions are based on behavior metrics, not tag-only telemetry.

### Phase L3: Ladder Evaluation V0

Goal: establish repeatable ladder-like evaluation.

Required capabilities:

- built-in opponent pool;
- scripted archetype opponent pool;
- AI Arena/local-play or upload-ready path;
- repeated matches;
- evaluation report.

Metrics:

- win rate;
- crash rate;
- timeout rate;
- game duration;
- build completion;
- first scout time;
- first attack time;
- combat count;
- units killed/lost;
- defense response count;
- strategy adaptation count.

### Phase L4: Learning-Augmented Modules

Goal: introduce learning modules without blocking L0-L2.

Candidate directions:

- replay/log imitation for build timing;
- learned opponent model;
- combat predictor;
- micro-control support branch via SMAC/custom scenarios.

These are not blockers for L0-L2, but the architecture should preserve interfaces for them.

## Execution Rules

- Do not execute multiple phases at once.
- Do not claim ladder readiness until L0 is validated.
- Do not claim gameplay quality improvement until L1/L2 metrics support it.
- Do not claim opponent modeling improves match outcomes until behavior or result ablations support it.
- Keep research prototypes out of `src/sc2bot/`.
- Keep evaluation orchestration out of bot decision logic.

## Next Recommended Phase

Start Phase L0: Ladder Readiness.
