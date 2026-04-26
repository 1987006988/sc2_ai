# R6 Frontier Closeout Report

Date: 2026-04-26

## Final Accepted Claim

We built and validated a replay-trained temporal opponent belief system for
StarCraft II partial observability. The learned belief beats non-learning
offline comparators, changes bounded online macro behavior in matched internal
evaluation, and has positive support on a narrow AI Arena-compatible local
bot-vs-bot external slice.

## Evidence Stack

### Offline

- report:
  - `artifacts/reports/r6_learned_belief_training/report.md`
- checkpoint:
  - `artifacts/reports/checkpoints/r6_checkpoint_I_learned_belief_gate.md`
- benchmark result:
  - `research/r6_temporal_belief/eval/results/r6_temporal_model_v0.json`

Accepted offline summary:

- learned holdout aggregate: `1.000`
- runtime-aligned rule-based: `0.825`
- static prior: `0.500`

### Internal

- report:
  - `artifacts/reports/r6_internal_paired/report.md`
- checkpoint:
  - `artifacts/reports/checkpoints/r6_checkpoint_J_internal_frontier_gate.md`
- accepted paired summaries:
  - `data/logs/evaluation/r6_internal_paired/easy/r6_internal_paired_easy_repair5_20260426/summary.json`
  - `data/logs/evaluation/r6_internal_paired/medium/r6_internal_paired_medium_repair5_20260426/summary.json`

Accepted internal summary:

- easy:
  - baseline `2/3`
  - comparator `2/3`
  - learned `2/3`
- medium:
  - baseline `1/3`
  - comparator `0/3`
  - learned `1/3`

### External

- report:
  - `artifacts/reports/r6_external_eval/report.md`
- accepted external summary:
  - `data/logs/evaluation/r6_external_eval/r6_external_house_bots_repair2_20260426/summary.json`

Accepted external summary:

- baseline vs external comparator house bot: `Tie`
- comparator vs external comparator house bot: `Victory`
- learned vs external comparator house bot: `Victory`

## Boundary

This closeout accepts only a **single-feature** claim:

- learned temporal belief
- bounded response surface

It does not accept:

- second adaptive feature claims
- broader external generalization
- third-party house-bot generalization
- ladder competitiveness

## Deliverables

- results table:
  - `artifacts/reports/r6_frontier_closeout/results_table.md`
- ablation table:
  - `artifacts/reports/r6_frontier_closeout/ablation_table.md`
- replay/demo index:
  - `artifacts/reports/r6_frontier_closeout/replay_demo_index.md`
- claim boundary page:
  - `artifacts/reports/r6_frontier_closeout/claim_boundary.md`
- model card:
  - `research/r6_temporal_belief/cards/model_card.md`
- dataset card:
  - `research/r6_temporal_belief/cards/dataset_card.md`
