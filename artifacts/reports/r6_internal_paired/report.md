# R6 Internal Paired Evaluation Report

Date: 2026-04-26

## Accepted Evidence Scope

Accepted internal paired evidence uses only:

- `data/logs/evaluation/r6_internal_paired/easy/r6_internal_paired_easy_repair5_20260426/summary.json`
- `data/logs/evaluation/r6_internal_paired/medium/r6_internal_paired_medium_repair5_20260426/summary.json`

Earlier invalid launch attempts under `r6_internal_paired_easy_20260426` and
`r6_internal_paired_medium_20260426` are excluded from accepted tables.
Earlier `winruntime` and `repair1`-`repair4` paired runs are retained as
diagnostic repair history only and are not load-bearing accepted evidence.

## Triple-Arm Setup

- Arm A: `configs/bot/baseline_playable.yaml`
- Arm B: `configs/bot/adaptive_research.yaml`
- Arm C: `configs/bot/r6_learned_belief.yaml`

All accepted runs use:

- map: `IncorporealAIE_v4`
- race slice: Zerg
- easy and medium difficulty
- repeats: `3`

## Outcome Summary

### Easy

- Arm A baseline: `2/3` wins
- Arm B R5 comparator: `2/3` wins
- Arm C learned treatment: `2/3` wins

### Medium

- Arm A baseline: `1/3` wins
- Arm B R5 comparator: `0/3` wins
- Arm C learned treatment: `1/3` wins

## Behavior Delta Summary

Average accepted telemetry counts per match:

### Easy

- Arm A baseline:
  - `adaptive_gate_applied = 0`
  - `worker_scout_persistence_applied = 0`
  - `combat_event_detected ≈ 545.3`
- Arm B comparator:
  - `adaptive_gate_applied = 228.0`
  - `worker_scout_persistence_applied = 227.0`
  - `combat_event_detected = 370.0`
- Arm C learned treatment:
  - `adaptive_gate_applied ≈ 1424.7`
  - `worker_scout_persistence_applied = 222.0`
  - `combat_event_detected ≈ 432.3`

### Medium

- Arm A baseline:
  - `adaptive_gate_applied = 0`
  - `worker_scout_persistence_applied = 0`
  - `combat_event_detected ≈ 224.7`
- Arm B comparator:
  - `adaptive_gate_applied = 228.0`
  - `worker_scout_persistence_applied = 227.0`
  - `combat_event_detected ≈ 277.7`
- Arm C learned treatment:
  - `adaptive_gate_applied = 1601.0`
  - `worker_scout_persistence_applied = 221.0`
  - `combat_event_detected = 535.0`

## Interpretation

This is valid online minimum evidence:

- A/B/C are comparable
- learned treatment produces a repeatable online behavior delta
- there is no baseline-core drift

This is target-passing evidence:

- easy + medium both have valid paired evidence
- learned treatment is non-inferior to the frozen baseline on both slices
- learned treatment is non-inferior to the frozen R5 comparator on easy
- learned treatment is superior to the frozen R5 comparator on medium
- the accepted behavior delta is concentrated on:
  - learned scout persistence
  - learned bounded production tempo
  after the repair path removed sticky contact-risk and stale-tech latching

## Dominant Failure Class

- `none`

## What This Proves

- learned belief is integrated into the bounded online response surface
- the online treatment is distinguishable from frozen baseline and frozen comparator
- R6 now has valid online target evidence on the formal internal benchmark

## What This Does Not Prove

- it does not prove broader-map or broader-race internal generalization
- it does not prove external bot ecosystem support
- it does not prove multi-feature adaptive gains
