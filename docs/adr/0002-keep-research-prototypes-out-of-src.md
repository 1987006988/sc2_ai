# ADR-0002: Keep Research Prototypes Out of src

## Status

Accepted

## Context

The project has several research lines: opponent modeling, replay learning, SMAC / SMACv2, LLM coach, and combat prediction. Mixing these into the bot runtime would make the mainline unstable.

## Decision

All prototypes live in `research/`. Production bot code lives in `src/sc2bot/`. The mainline must not import from `research/`.

## Consequences

Positive:

- Mainline remains clean and runnable.
- Experiments can move quickly without breaking runtime.
- Promotion decisions are reviewable.

Negative:

- Some code may need to be rewritten during promotion.

## Verification

Tests and review should reject imports from `research/` inside `src/sc2bot/`.
