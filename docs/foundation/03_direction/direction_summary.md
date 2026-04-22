# Direction Summary

## Current Mainline

The current mainline is a layered hybrid full-game StarCraft II bot.

Production runtime code lives only in `src/sc2bot/`.

## Core Direction

- Mainline: layered hybrid full-game bot.
- Primary phase-1 research feature: opponent modeling / hidden-state inference.
- Data line: replay / imitation learning.
- Support line: SMAC / SMACv2 micro experiments.
- Auxiliary line: LLM replay analysis / coach tooling.
- Optional phase-1 showcase enhancement: replay summary.

## Why This Direction Was Chosen

- It supports a runnable bot early.
- It fits limited engineering and compute budgets.
- It preserves research value without forcing end-to-end RL as the starting point.
- It keeps prototypes and benchmarks out of the production bot mainline.

## One-line Positioning

Build a full-game SC2 AI that reads the opponent under fog of war, adapts strategy online, and has post-match explainable replay capability.

## Phase 1 Validation Requirement

Phase 1 must include at least one fixed-opponent-pool ablation:

- without opponent model;
- with opponent model.

This comparison is required for validation and is not optional.

## What We Are Not Doing Now

- No AlphaStar-like end-to-end mainline.
- No full world model as phase-1 mainline.
- No LLM real-time control layer.
- No SMAC benchmark code inside `src/sc2bot/`.

## Boundary Reminder

Interview-oriented positioning is a presentation layer. It does not replace the engineering definition of the project, and it does not relax the boundary between mainline, research, and evaluation.
