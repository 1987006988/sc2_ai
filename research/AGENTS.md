# research AGENTS.md

This directory is for prototypes, notebooks, ablations, and research experiments.

## Rules

- Code here is not production by default.
- `src/sc2bot/` must not import from `research/`.
- Each research subdirectory needs a `README.md` explaining goal, status, data inputs, and promotion path.
- Keep experiment outputs in `reports/` or `artifacts/`, not in mainline code.
- If a prototype should enter mainline, create a plan and follow promotion rules in root `AGENTS.md`.

## Phase 1 Research Priority

Primary: opponent modeling / hidden-state inference prototype.

Secondary or optional:

- replay feature extraction;
- combat predictor;
- SMAC / SMACv2 baseline checks;
- LLM replay analysis.
