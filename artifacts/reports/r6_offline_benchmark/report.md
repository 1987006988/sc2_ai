# R6 Offline Benchmark Report

Date: 2026-04-26
Task: `r6_task_005_run_offline_hidden_state_benchmark`

## Status

- `blocked`

## Blocking Reason

Current best failure classification:

- `dataset_contract_frozen_but_holdout_inputs_not_materialized`

Observed state:

- dataset contract exists
- split policy exists
- leakage validation command exists
- hidden-state label and baseline pipeline skeleton exists
- but no materialized public replay corpus / benchmark dataset has been ingested
  into a benchmark-ready train/val/test split

## Why This Is A Real Blocker

`task_005` requires a first valid offline benchmark.

Current local sources are insufficient for that claim:

- local accepted R4 / R5 replay artifacts are explicitly restricted to
  `domain_anchor_only`
- no benchmark-ready public replay source has been materialized
- no holdout split with valid benchmark rows exists yet

Therefore:

- fixture subset validation from `task_004` is useful implementation evidence
- but it is not valid offline benchmark evidence

## What This Proves

- the repository is ready to begin real benchmark ingestion work
- the blocker is no longer missing contract or missing baseline skeleton
- the blocker is now concrete input availability for the first valid benchmark

## What This Does Not Prove

- it does not prove any offline leaderboard
- it does not prove leakage-safe benchmark execution
- it does not prove learned model readiness

## Next Allowed Action

- `r6_task_005_run_offline_hidden_state_benchmark` remains blocked
- the immediate repair target is to materialize benchmark-ready replay sources
  under the frozen dataset contract before claiming a valid offline benchmark
