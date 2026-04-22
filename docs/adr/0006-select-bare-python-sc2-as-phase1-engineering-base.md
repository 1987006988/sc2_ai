# ADR-0006: Select Bare python-sc2 as the Phase-1 Engineering Base

## Status

Accepted

## Context

Phase 1 needs a practical engineering base for a runnable full-game bot. The candidate options were:

- Ares-sc2;
- bare python-sc2.

In the current local environment, neither `ares` nor `sc2` is installed, and dry-run package resolution attempts do not currently provide either package. This means the phase-1 decision must prefer the lower-dependency, more direct target.

## Decision

Use bare python-sc2 as the phase-1 engineering base target.

Ares-sc2 remains a valid future enhancement candidate, but it is not required to begin phase-1 implementation.

## Rationale

- Ares-sc2 is an additional layer on top of python-sc2.
- Choosing bare python-sc2 keeps the runtime integration target simpler.
- The current project already has its own runtime, manager, and telemetry structure, so a thinner integration base reduces coupling risk.
- This choice does not change the approved mainline architecture.

## Consequences

Positive:

- Lower dependency surface for phase 1.
- Cleaner alignment with the project's own manager architecture.
- Fewer assumptions while local runtime validation is still incomplete.

Negative:

- Some convenience utilities available in Ares-sc2 will need to be added later or replaced with project-local implementations.

## Verification

This ADR is working if:

- local runtime integration targets bare python-sc2 first;
- evaluation and bot startup continue to advance without requiring Ares-sc2;
- Ares-specific features are not assumed in phase-1 plans.
