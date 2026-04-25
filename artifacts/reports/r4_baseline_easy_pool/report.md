# R4 Baseline Easy Pool Batch Report

Date: 2026-04-25
Task: `task_013_baseline_easy_pool_batch_evaluation`

## Batch Design

- config: `configs/evaluation/r4_baseline_easy_pool_batch.yaml`
- bot config: `configs/bot/baseline_playable.yaml`
- map slice: `IncorporealAIE_v4`
- opponent slice:
  - `builtin_easy_terran`
  - `builtin_easy_zerg`
  - `builtin_easy_protoss`
- repeats: `2`
- intended valid batch size: `6`

## Evidence Separation

Two execution attempts exist under the same run root:

1. invalid first attempt:
   - `6` runs
   - all `launch_error`
   - shared failure reason: `SC2PATH is not set`
   - classification: `invalid_evidence`
   - action taken: identical rerun with corrected environment contract
2. valid rerun:
   - `6` runs
   - all real local matches launched successfully
   - these `6` runs are the only load-bearing evidence for R4 judgment

## Valid Rerun Outcome Summary

- total valid runs: `6`
- valid wins: `0`
- valid defeats: `6`
- opponent outcomes:
  - Terran easy: `0/2` wins
  - Zerg easy: `0/2` wins
  - Protoss easy: `0/2` wins

## Valid Rerun Gameplay Chain Summary

Across the `6` valid runs:

- `gateway_build_success = 6`
- `cybernetics_core_build_success = 6`
- `unit_created_detected = 60`
- `army_presence_changed = 60`
- `combat_event_detected = 99`

Per valid run:

- every run reached build-chain continuation beyond pure survival scaffold
- every run produced friendly combat-unit creation signals
- every run produced documented army-presence changes
- every run produced post-execution contact/combat-neighbor telemetry
- every run still ended in `Result.Defeat`

Representative per-run maxima:

- `max_own_army_count` ranged from `8` to `9`

## Interpretation

This batch does **not** show a prerequisite regression:

- build chain still exists
- army presence still exists
- tactical/contact-neighbor evidence still exists

But this batch also does **not** satisfy the R4 minimum claim:

- there is no uncontested real win
- there is no sufficiently strong near-win evidence recorded in the current artifact set
- the easy slice result is uniformly defeat, not repeated success

So the dominant R4 blocker is no longer army-core or tactical-core existence.
It is now an outcome-level baseline weakness:

- the bot can build, produce, rally, and reach contact-neighbor states
- but it still cannot convert that chain into wins or convincing near-win evidence on the designated easy slice
- the valid rerun also points to a likely sustained macro / spending sub-problem:
  - each valid run ended with roughly `3405-3530` minerals banked
  - each valid run recorded only `10` `unit_created_detected` events
  - end-state `own_army_count` stayed in the `2-9` range instead of converting the bank into a clearly dominant army

## Failure Classification

Current best fit:

- `logic_failure`

Reasoning:

- invalid evidence was already isolated and rerun
- no systemic prerequisite regression appears in the valid rerun
- the remaining failure is the bot's inability to turn an apparently complete gameplay chain into acceptable baseline outcomes
- within that broader outcome failure, the clearest repair lead is weak sustained production / spending rather than missing build-chain or missing tactical contact

## Minimum Gate

`failed`

Reason:

- R4 minimum requires at least one uncontested real win or very strong near-win evidence
- the valid easy-slice rerun produced `0/6` wins
- current artifacts do not justify upgrading any defeat into a strong near-win claim

## Target Gate

`failed`

Reason:

- repeated wins or equivalently strong repeated advantage evidence did not appear
- the easy slice does not currently support Level 1 acceptance

## Stretch Gate

`failed`

Reason:

- baseline is not yet stable enough to act as an accepted adaptive-evaluation control

## What This Proves

- the invalid `SC2PATH` batch can be separated cleanly from the valid rerun
- the valid rerun confirms the bot is no longer only a pure diagnostic scaffold
- build-chain, army, and tactical/contact-neighbor signals persist in a real easy-slice batch
- the dominant remaining R4 blocker is outcome-level baseline weakness, not prerequisite regression

## What This Does Not Prove

- it does not prove Level 1 playable baseline acceptance
- it does not prove repeated wins
- it does not prove a strong near-win without further explicit evidence
- it does not justify entering adaptive paired evaluation

## Evidence Paths

- `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/summary.json`
- valid rerun match roots:
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-0f334f9e`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-f2cd367b`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-cad81c16`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-fbdfe964`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-0c596e6f`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-5e392734`
- invalid first-attempt roots:
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-08b96bd7`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-d7bd716a`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-4122b658`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-56db4197`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-011a1818`
  - `data/logs/evaluation/r4_baseline_easy_pool_batch/r4_baseline_easy_pool_batch_20260425/reallaunch-641abec4`
