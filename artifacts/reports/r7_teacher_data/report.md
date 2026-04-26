# R7 Teacher Data Report

Date: 2026-04-27
Task: `r7_task_007_materialize_teacher_replay_dataset`

## Result

Teacher dataset v0 was materialized from the acquired DI-star replay corpus.

## Source

- source id:
  - `distar_zvz_agent_platform`
- replay source:
  - `third_party/strong_bots/DI-star/data/replays`
- source commit:
  - `12b1c69350ad41e17895c602a66a52d98dd58452`

## Dataset Boundary

This dataset is a **teacher-proxy command-event dataset**.

It does not claim:

1. full hidden-state ground truth at every timestep
2. true counterfactual causality labels
3. production-ready online intervention supervision

It does support:

1. hidden-state proxy tasks
2. macro-action proxy tasks
3. future-outcome proxy tasks

## Materialized Outputs

- `data/r7/teacher_dataset/train.jsonl`
- `data/r7/teacher_dataset/val.jsonl`
- `data/r7/teacher_dataset/test.jsonl`
- `data/r7/teacher_dataset_manifest.json`
- `research/r7_world_model/cards/dataset_card.md`

## Dataset Summary

- replay count:
  - `16`
- split counts:
  - train: `12`
  - val: `10`
  - test: `10`
- label families materialized:
  - hidden-state proxy:
    - `enemy_opening_class`
    - `enemy_tech_path`
  - macro-action proxy:
    - `macro_action_label`
    - `production_tempo_label`
  - future-outcome proxy:
    - `future_winner`
    - `future_game_length_bucket`
    - `future_pressure_proxy`

## Gate Result

- minimum gate: `passed`
- target gate: `passed`
- stretch gate: `failed`

## Why Stretch Fails

1. dataset only uses the first acquired strong source
2. there is no second teacher source mixed in yet
3. labels are proxy-level rather than richer replay+log fused labels
