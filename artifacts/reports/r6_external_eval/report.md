# R6 External Evaluation Report

Date: 2026-04-26

## Accepted Evidence Scope

Accepted external evidence uses only:

- `configs/evaluation/r6_external_house_bots.yaml`
- `data/logs/evaluation/r6_external_eval/r6_external_house_bots_repair2_20260426/summary.json`
- `data/logs/evaluation/r6_external_eval/r6_external_house_bots_repair2_20260426/reallaunch-cb7356ae/match_result.json`
- `data/logs/evaluation/r6_external_eval/r6_external_house_bots_repair2_20260426/reallaunch-be504631/match_result.json`
- `data/logs/evaluation/r6_external_eval/r6_external_house_bots_repair2_20260426/reallaunch-e450406f/match_result.json`

Excluded diagnostic history:

- `r6_external_house_bots_formal_20260426`
- `r6_external_house_bots_repair1_20260426`

Those earlier runs are invalid because the first bot-vs-bot implementation still
used a launch/exit path that could downgrade completed matches into
`launch_error`.

## External Environment Contract

This is a narrow accepted external slice:

- environment type: AI Arena-compatible local bot-vs-bot
- map: `IncorporealAIE_v4`
- external opponent contract:
  - `opponent_type = bot`
  - fixed external opponent config:
    `configs/bot/adaptive_research.yaml`
  - opponent id:
    `external_frozen_r5_comparator_house_bot`
- focal arms:
  - Arm A `configs/bot/baseline_playable.yaml`
  - Arm B `configs/bot/adaptive_research.yaml`
  - Arm C `configs/bot/r6_learned_belief.yaml`
- repeats: `1`

This is accepted as an **equivalent external bot slice**. It is not a claim of
third-party downloadable house-bot generalization.

## Outcome Summary

- Arm A frozen baseline vs external comparator house bot:
  - `Tie`
- Arm B frozen R5 comparator vs external comparator house bot:
  - `Victory`
- Arm C learned treatment vs external comparator house bot:
  - `Victory`

## Behavior Delta Summary

Per-match focal telemetry counts:

- Arm A frozen baseline:
  - `adaptive_gate_applied = 0`
  - `worker_scout_persistence_applied = 0`
  - `combat_event_detected = 43`
- Arm B frozen R5 comparator:
  - `adaptive_gate_applied = 226`
  - `worker_scout_persistence_applied = 225`
  - `combat_event_detected = 49`
- Arm C learned treatment:
  - `adaptive_gate_applied = 1578`
  - `worker_scout_persistence_applied = 220`
  - `combat_event_detected = 99`

## Interpretation

This is target-passing external evidence:

- at least one valid external slice exists
- the accepted slice is not built-in AI
- the learned treatment produces a positive external result
- the learned treatment remains directionally consistent with the accepted
  internal claim:
  - stronger learned gate activity than frozen baseline
  - positive outcome on the same external slice

This is still a bounded external claim:

- the accepted external slice uses an AI Arena-compatible local bot-vs-bot
  environment
- the fixed external opponent is the frozen R5 comparator packaged as a
  house-bot-equivalent opponent
- this does not prove third-party house-bot generalization

## Dominant Failure Class

- `none`

## What This Proves

- the learned temporal belief treatment is not only a built-in-AI artifact
- the accepted method survives one valid external bot-vs-bot slice
- external evidence is now available for frontier closeout

## What This Does Not Prove

- it does not prove broader external generalization
- it does not prove performance against third-party downloadable house bots
- it does not prove tournament or ladder competitiveness
