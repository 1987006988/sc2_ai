# R7 External Validation Report

Date: 2026-04-27
Status: completed
Task: `r7_task_016_run_external_bot_ecosystem_validation`

## Accepted Evidence Scope

Accepted external evidence uses only:

- `configs/evaluation/r7_external_validation.yaml`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/summary.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/baseline/match_result.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/world/match_result.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/world/advisor_stats.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/world/match.SC2Replay`

Excluded invalid probe:

- `external_warpgate_probe`

Why invalid:

1. the external opponent crashed on unseen ability id `4132`
2. the opponent-side runtime fault makes that slice non-comparable

## External Environment Contract

This is a bounded but valid external slice:

- environment class:
  - `downloaded_bot_repo_external_example_slice`
- substrate:
  - `sludge_revived_current_patch_house_bot`
- external opponent:
  - `worker_rush_example_bot`
- map:
  - `KairosJunctionLE`
- game time limit:
  - `420`

Arms included in the accepted external evidence:

1. Arm A raw strong substrate
2. Arm C learned world-model advisor

Arm B is not part of this accepted external slice. The protocol permits A/C
comparability when full A/B/C is not load-bearing for the external claim.

## Outcome Summary

- Arm A raw strong substrate vs worker_rush external bot:
  - `Victory`
- Arm C learned world-model advisor vs worker_rush external bot:
  - `Victory`

## Behavior Delta Summary

Arm A:

- no advisor applied
- terminal mode:
  - `attack`
- terminal economy / army:
  - `townhalls = 2`
  - `army_count = 20`
  - `army_value = 650`

Arm C:

- `advisor/applied_count = 1006`
- action mix:
  - `add_tech = 694`
  - `defensive_hold = 231`
  - `increase_production_tempo = 81`
- terminal mode:
  - `attack`
- terminal economy / army:
  - `townhalls = 2`
  - `army_count = 26`
  - `army_value = 1100`

## Interpretation

This is target-passing external evidence:

1. at least one valid external slice exists
2. the slice is not built-in AI
3. Arm C is non-inferior to Arm A on the accepted external slice
4. the direction is consistent with the internal result because the learned arm
   still expresses a real bounded macro behavior delta on the same strong
   substrate

This is still a bounded external claim:

1. the external opponent is a downloaded repo-packaged example bot, not an AI
   Arena downloadable ladder bot
2. the accepted external evidence is only one slice
3. this does not prove broader external generalization

## Artifact Note

The accepted external runner can exit with:

- `run_error = SystemExit(2)`

after replay save and after telemetry save when the python-sc2 external-bot
cleanup path closes both bot clients. This slice is still accepted because:

1. replay exists
2. result JSON exists
3. telemetry exists
4. the focal match result is explicit and consistent across artifacts

## What This Proves

1. the R7 method is not only an internal strong-substrate artifact
2. the learned world-model advisor survives one valid external bot slice
3. the external slice stays within the same downloaded strong substrate family
   and remains auditable

## What This Does Not Prove

1. it does not prove AI Arena house-bot generalization
2. it does not prove third-party downloadable bot robustness
3. it does not prove tournament or ladder competitiveness
