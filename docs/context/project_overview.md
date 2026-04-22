# Project Overview

This project builds a layered hybrid full-game StarCraft II bot.

## Mainline

The mainline is a runnable full-game bot in `src/sc2bot/`.

## Phase 1 Focus

- runnable skeleton;
- local smoke evaluation loop;
- minimal telemetry;
- replay metadata;
- stable config loading;
- opponent model interface;
- first rule-based opponent modeling prototype.

## Research Feature

Phase 1 research feature: opponent modeling / hidden-state inference.

## Supporting Lines

- replay / imitation learning as data line;
- SMAC / SMACv2 as micro research line;
- LLM replay analysis as auxiliary coach layer.

## Validation Requirement

Phase 1 requires at least one fixed-opponent-pool comparison:

- without opponent model;
- with opponent model.

## Showcase Enhancements

The project may add structured strategy explanation and replay summary for presentation, but these do not block phase-1 mainline completion.

## Document Layering

- `docs/foundation/` stores the historical inputs and route lock-in materials.
- `docs/context/` stores the current living project consensus.
