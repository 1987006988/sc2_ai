# ADR-0005: Use Interview-oriented Positioning Without Changing Mainline

## Status

Accepted

## Context

The project benefits from a strong presentation narrative for interviews and demos, but the engineering mainline already has clear boundaries: layered hybrid full-game bot, opponent modeling as the primary phase-1 research feature, and strict separation between mainline and research.

## Decision

Adopt an interview-oriented positioning layer in `docs/foundation/03_direction/`, but keep the engineering mainline unchanged.

Specifically:

- the mainline remains a layered hybrid full-game bot;
- opponent modeling remains the primary phase-1 research feature;
- replay summary and strategy explanation are showcase enhancements, not blockers;
- SMAC, LLM coach, replay-learning prototypes, and world-model work remain outside `src/sc2bot/` unless promoted later.

## Consequences

Positive:

- The project gains a stronger external narrative.
- Demo goals are clearer.
- The mainline remains stable and bounded.

Negative:

- Team members must distinguish between presentation goals and engineering commitments.

## Verification

This ADR is working if:

- route documents in `docs/foundation/03_direction/` reflect the new positioning;
- `AGENTS.md` remains concise and does not absorb interview prose;
- implementation work continues to prioritize runtime, evaluation, telemetry, and opponent modeling.
