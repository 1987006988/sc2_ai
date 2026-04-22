# Opponent Model Ablation Protocol

## Goal

Measure whether opponent modeling improves decision quality on a fixed opponent pool.

## Required Comparison

1. `without_opponent_model`
2. `with_opponent_model`

## Fixed Variables

- same race
- same map pool
- same evaluation runner
- same opponent pool
- same bot version except for opponent-model toggle

## Phase-1 Metrics

- match completion count
- win rate
- rush defense success rate
- strategy-switch count
- opponent-model prediction coverage

## Minimum Evaluation Output

- one evaluation summary for `without_opponent_model`
- one evaluation summary for `with_opponent_model`
- one short comparison note in `reports/`
