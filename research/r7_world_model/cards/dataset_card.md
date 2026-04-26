# R7 Teacher Dataset Card

Dataset id: `r7_teacher_dataset_v0_proxy`
Updated: 2026-04-27

## Source

- primary source:
  - acquired DI-star replay corpus
- source path:
  - `third_party/strong_bots/DI-star/data/replays`
- source commit:
  - `12b1c69350ad41e17895c602a66a52d98dd58452`

## Claim Boundary

This is a **teacher-proxy** dataset built from replay command events.

It is suitable for:

1. hidden-state proxy labels
2. macro-action proxy labels
3. future-outcome proxy labels
4. baseline leaderboard construction

It is not yet:

1. a full counterfactual dataset
2. a full omniscient state-action trajectory export
3. external-teacher-generalization evidence
