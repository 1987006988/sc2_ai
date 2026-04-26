# R6 Learned Belief Training Report

Date: 2026-04-26
Tasks:

- `r6_task_007_implement_temporal_belief_model_and_training_loop`
- `r6_task_008_train_and_evaluate_temporal_belief_model`

## Status

- `completed`

## Model

- model name: `temporal_gru_v0`
- architecture: `GRU + temporal summary inductive bias`
- checkpoint:
  - `artifacts/models/r6_temporal_belief/temporal_gru_v0.pt`

## Training Contract

- config:
  - `configs/research/r6_train_gru.yaml`
- train split:
  - `research/r6_temporal_belief/data/materialized/train.jsonl`
- val split:
  - `research/r6_temporal_belief/data/materialized/val.jsonl`
- test split:
  - `research/r6_temporal_belief/data/materialized/test.jsonl`

## Comparator Set

- `learned_temporal`
- `rule_based_runtime_aligned`
- `static_prior`

## Holdout Result Summary

Aggregate primary-task score:

- learned temporal val: `1.000000`
- learned temporal test: `1.000000`
- rule-based val: `0.900000`
- rule-based test: `0.825000`
- static prior val: `0.600000`
- static prior test: `0.500000`

Primary task bundle:

- `opening_class`
- `hidden_tech_path`
- `hidden_army_bucket`
- `future_contact_risk`
- `next_macro_threat_indicator`

Test split per-task balanced accuracy:

- `opening_class`
  - learned: `1.0`
  - rule-based: `0.333333`
  - static prior: `0.5`
- `hidden_tech_path`
  - learned: `1.0`
  - rule-based: `0.791667`
  - static prior: `0.5`
- `hidden_army_bucket`
  - learned: `1.0`
  - rule-based: `1.0`
  - static prior: `0.5`
- `future_contact_risk`
  - learned: `1.0`
  - rule-based: `1.0`
  - static prior: `0.5`
- `next_macro_threat_indicator`
  - learned: `1.0`
  - rule-based: `1.0`
  - static prior: `0.5`

## Interpretation

This is sufficient for the current R6.2 target gate:

- the learned temporal treatment exceeds the static prior baseline
- it also exceeds the current runtime-aligned rule-based comparator on the
  primary offline task bundle
- the training / checkpoint / inference loop is reproducible from config

This is not yet the full stretch claim:

- only one architecture is accepted
- no multi-history ablation is accepted yet
- calibration / uncertainty coverage is not yet a load-bearing accepted result

## What This Proves

- R6 now has a trainable temporal belief model with a reproducible checkpoint
  loop
- the first learned temporal model beats the baseline floor on the current
  holdout benchmark
- Phase R6.2 can advance to online integration planning

## What This Does Not Prove

- it does not prove online behavior gain yet
- it does not prove external validity yet
- it does not prove this architecture is the only or best temporal model

## Evidence Paths

- `configs/research/r6_train_gru.yaml`
- `research/r6_temporal_belief/train/train_temporal_model.py`
- `research/r6_temporal_belief/eval/results/r6_temporal_model_v0.json`
- `research/r6_temporal_belief/cards/model_card.md`
- `artifacts/models/r6_temporal_belief/temporal_gru_v0.pt`
