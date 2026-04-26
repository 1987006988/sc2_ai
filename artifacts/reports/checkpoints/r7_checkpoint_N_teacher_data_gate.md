# R7 Checkpoint N: Teacher Data Gate

Date: 2026-04-27

## Reviewed Tasks

- `r7_task_007_materialize_teacher_replay_dataset`
- `r7_task_008_build_teacher_benchmark_and_baselines`

## Evidence Paths

- `data/r7/teacher_dataset/train.jsonl`
- `data/r7/teacher_dataset/val.jsonl`
- `data/r7/teacher_dataset/test.jsonl`
- `data/r7/teacher_dataset_manifest.json`
- `configs/research/r7_teacher_dataset.yaml`
- `configs/research/r7_teacher_benchmark.yaml`
- `research/r7_world_model/eval/results/r7_teacher_benchmark_v0.json`
- `research/r7_world_model/cards/dataset_card.md`
- `artifacts/reports/r7_teacher_data/report.md`
- `artifacts/reports/r7_teacher_benchmark/report.md`
- `artifacts/reports/checkpoints/r7_checkpoint_N_teacher_data_gate.md`

## Gate Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = r7_task_010_train_counterfactual_macro_world_model`

## Why It Passes

1. a replay-derived teacher dataset was materialized with replay-level split assignment
2. hidden-state, macro-action, and future-outcome proxy labels are all extractable
3. the offline benchmark ran end-to-end on holdout splits
4. the baseline leaderboard exists and is not degenerate

## Why Stretch Fails

1. the dataset is still single-source
2. the labels are teacher-proxy rather than richer replay+log fused supervision
3. the benchmark does not yet include calibration, history-length, or per-source ablations

## Claim Boundary

This checkpoint accepts:

1. teacher-data materialization
2. benchmark validity
3. baseline floor establishment

This checkpoint does not accept:

1. full counterfactual world-model supervision
2. online intervention readiness
3. external bot evaluation readiness

## Invalid Evidence Excluded

1. no fabricated local run data is mixed into the teacher dataset
2. no downloaded strong-bot raw strength is treated as our contribution
3. no external evaluation data is mixed into the training holdout
