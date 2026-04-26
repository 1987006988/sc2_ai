# R7 Frontier Closeout Report

Date: 2026-04-27
Status: completed
Task: `r7_task_017_prepare_frontier_interview_evidence_pack`

## Accepted Scope

R7 is accepted as a bounded frontier result with:

1. teacher-data offline benchmark through `r7_checkpoint_N`
2. scratch-first offline world-model through `r7_checkpoint_O`
3. strong-substrate online intervention through `r7_checkpoint_P`
4. one valid external bot slice through `r7_task_016`

## Evidence Stack

### Offline

- teacher benchmark:
  - `research/r7_world_model/eval/results/r7_teacher_benchmark_v0.json`
- accepted scratch ensemble:
  - `artifacts/models/r7_world_model/scratch_ensemble_v0.json`
- offline reports:
  - `artifacts/reports/r7_teacher_benchmark/report.md`
  - `artifacts/reports/r7_world_model_training/report.md`

### Internal Online

- accepted internal summary:
  - `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/summary.json`
- online report:
  - `artifacts/reports/r7_online_integration/report.md`

### External

- accepted external summary:
  - `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/summary.json`
- external report:
  - `artifacts/reports/r7_external_validation/report.md`

## One-Line Result

The project now has a replay-trained, scratch-first macro world-model line that
is:

1. stronger than the benchmark floor offline,
2. behaviorally active and outcome-positive on the accepted strong substrate
   internally,
3. externally supported by one valid downloaded-bot slice.

## Boundaries

Still not accepted:

1. broader external generalization
2. AI Arena house-bot or downloadable-bot robustness
3. ladder competitiveness
4. full non-proxy counterfactual supervision

## Supporting Closeout Files

- results table:
  - `artifacts/reports/r7_frontier_closeout/results_table.md`
- claim boundary:
  - `artifacts/reports/r7_frontier_closeout/claim_boundary.md`
- replay/demo index:
  - `artifacts/reports/r7_frontier_closeout/replay_demo_index.md`
