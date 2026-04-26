# R6 Offline Benchmark Report

Date: 2026-04-26
Task: `r6_task_005_run_offline_hidden_state_benchmark`

## Status

- `completed`

## Benchmark Inputs

Materialized under the frozen R6 dataset contract:

- train:
  - `local_phase_a_chunk_1_historical_corpus`
  - `local_phase_a_chunk_2_historical_corpus`
- val:
  - `local_phase_a_chunk_3_historical_corpus`
- test:
  - `local_phase1d_ablation_historical_corpus`
  - `local_phase1e_ablation_historical_corpus`

Accepted R4/R5 anchors remain excluded from holdout use:

- `local_r4_level1_baseline_artifacts`
- `local_r5_adaptive_paired_artifacts`

Materialized split files:

- `research/r6_temporal_belief/data/materialized/train.jsonl`
- `research/r6_temporal_belief/data/materialized/val.jsonl`
- `research/r6_temporal_belief/data/materialized/test.jsonl`

Split counts:

- train: `16`
- val: `8`
- test: `14`

## Comparator Set

- `rule_based`
- `static_prior`
- `shallow_temporal`

## Result Summary

Validation result:

- `R6_OFFLINE_BENCHMARK_VALID`

Holdout leaderboard summary:

- val:
  - `rule_based`: `1.000000`
  - `shallow_temporal`: `1.000000`
  - `static_prior`: `0.666667`
- test:
  - `rule_based`: `1.000000`
  - `shallow_temporal`: `1.000000`
  - `static_prior`: `0.583333`

Task variability observed:

- non-degenerate:
  - `opening_class`
  - `hidden_army_bucket`
  - `future_contact_risk`
  - `next_macro_threat_indicator`
- partially degenerate in v0:
  - `hidden_tech_path`
  - `future_expansion_within_horizon`

## Interpretation

This v0 benchmark is now valid as an offline benchmark floor:

- leakage-safe splits are materialized
- baseline comparators run end-to-end on non-fixture holdout inputs
- accepted R4/R5 evidence remains fenced off from holdout tables

This v0 benchmark is not yet a strong discriminative research benchmark:

- `rule_based` and `shallow_temporal` tie on current labels
- some tasks are still low-diversity or degenerate on the current local corpus
- no learned model has been evaluated yet

## What This Proves

- R6 now has a first valid offline benchmark
- a baseline leaderboard exists on real historical holdout inputs
- Phase R6.1 can advance to learned temporal model implementation

## What This Does Not Prove

- it does not prove public replay ingestion yet
- it does not prove calibration or uncertainty coverage
- it does not prove the current benchmark is the final R6 offline benchmark
- it does not prove any learned temporal model gain

## Evidence Paths

- `research/r6_temporal_belief/data/source_manifest.yaml`
- `research/r6_temporal_belief/data/dataset_manifest.json`
- `research/r6_temporal_belief/data/materialized/train.jsonl`
- `research/r6_temporal_belief/data/materialized/val.jsonl`
- `research/r6_temporal_belief/data/materialized/test.jsonl`
- `research/r6_temporal_belief/datasets/materialize_local_benchmark.py`
- `research/r6_temporal_belief/eval/run_offline_benchmark.py`
- `research/r6_temporal_belief/eval/results/r6_offline_benchmark_v0.json`

## Gate Result

- minimum gate: `passed`
- target gate: `passed`
- stretch gate: `failed`

Stretch remains failed because:

- calibration / uncertainty coverage is not yet in the accepted v0 result
- benchmark task diversity is still limited on part of the bundle
