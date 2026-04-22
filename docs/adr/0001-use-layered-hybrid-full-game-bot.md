# ADR-0001: Use Layered Hybrid Full-game Bot

## Status

Accepted

## Context

The project goal is to build a runnable and research-relevant StarCraft II full-game bot under limited engineering and compute resources.

## Decision

Use a layered hybrid architecture:

- rules and programmatic planning for initial macro and runtime stability;
- stable manager interfaces;
- opponent modeling as the first research feature;
- learning modules promoted only after prototype validation.

## Consequences

Positive:

- Faster first runnable bot.
- Clear module boundaries.
- Research features can be added incrementally.

Negative:

- Requires careful boundary discipline.
- Early bot strength may depend on handcrafted rules.

## Verification

The architecture works if a skeleton bot can run through the evaluation loop and later accept opponent model outputs without rewriting runtime.
