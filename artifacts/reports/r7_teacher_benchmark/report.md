# R7 Teacher Benchmark Report

Date: 2026-04-27
Task: `r7_task_008_build_teacher_benchmark_and_baselines`

## Result

The first valid R7 teacher benchmark ran end-to-end on the materialized holdout
split.

## Benchmark Boundary

This benchmark is a **teacher-proxy benchmark** built from replay command
events, not a full counterfactual world-model benchmark yet.

## Comparator Set

1. `static_prior`
2. `rule_based`
3. `shallow_temporal`

## Output

- `research/r7_world_model/eval/results/r7_teacher_benchmark_v0.json`

## Leaderboard Summary

Validation split:

- `shallow_temporal = 0.524008`
- `rule_based = 0.511838`
- `static_prior = 0.388889`

Test split:

- `rule_based = 0.563704`
- `static_prior = 0.416667`
- `shallow_temporal = 0.337778`

Interpretation:

1. the benchmark is non-degenerate
2. the baseline floor is established
3. the current teacher-proxy task bundle is strong enough to justify moving to
   learned world-model training

## Gate Result

- minimum gate: `passed`
- target gate: `passed`
- stretch gate: `failed`

## Why Stretch Fails

1. no calibration diagnostics yet
2. no per-source ablation yet
3. no history-length analysis yet
