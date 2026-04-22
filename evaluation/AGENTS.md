# evaluation AGENTS.md

This directory owns evaluation orchestration, fixed opponent pools, batch runs, and metrics.

## Rules

- Do not put bot decision logic here.
- Evaluation may run the bot through stable entrypoints.
- Evaluation configs must be versioned under `configs/evaluation/`.
- Opponent pools must be explicit and repeatable.
- Every batch run should write metadata, results, and logs.
- Metrics should be stable enough for regression comparison.

## Phase 1 Focus

- smoke evaluation skeleton;
- fixed local opponent pool;
- match result schema;
- basic metrics collection.
