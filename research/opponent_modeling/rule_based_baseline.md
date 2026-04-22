# Rule-based Opponent Model Baseline

## Purpose

Provide the first non-null opponent-model baseline for phase-1 evaluation.

## Design

Use a small deterministic ruleset over scouting observations:

- if early enemy combat units are seen, raise `rush_risk`
- if few combat units but tech structures appear, raise `tech_risk`
- if early expansion is seen, lower `rush_risk` and mark `greedy_expand`
- if little information exists, keep low confidence and emit `scout_more`

## Why Rule-based First

- fast to implement;
- easy to inspect;
- easy to compare against null model;
- sufficient for the required first ablation.

## Promotion Rule

The rule-based baseline can stay in research until a stable interface and evaluation result justify updating the production implementation.
