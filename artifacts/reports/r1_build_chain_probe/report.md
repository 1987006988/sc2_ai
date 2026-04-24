# R1 Build Chain Probe Report

Date: 2026-04-24
Task: `task_005_real_build_chain_probe`

## Run

- run dir: `data/logs/evaluation/r1_build_chain_probe/reallaunch-ab4d1133`
- config: `configs/bot/baseline_playable.yaml`
- opponent: `builtin_easy_terran`
- map: `incorporeal_aie_v4`

## Artifact Completeness

- `match_result.json`: present
- `telemetry/events.jsonl`: present
- `match.SC2Replay`: present
- `preflight.json`: present
- `replay_metadata.json`: present

## Key Findings

Fair opportunity window was reached:

- `max_game_time = 321.43`
- `runtime_max_game_loop = 7200`

Opening build-chain evidence:

- `gateway_build_attempt = 1`
- `gateway_build_success = 1`
- `gateway_ready_inferred = true`
- first `gateway_ready_count > 0` seen by `game_time = 140.0`
- `assimilator_build_attempt = 1`
- `assimilator_build_success = 1`
- `cybernetics_core_build_attempt = 1`
- `cybernetics_core_build_success = 1`

Stretch-only forward signal:

- `combat_unit_production_attempt = 7`
- `combat_unit_production_success = 7`

## Minimum Gate

`passed`

Reason:

- Gateway-ready state was not inferred from command-only telemetry.
- It was evidenced by later telemetry payloads carrying `gateway_ready_count = 1`
  in a fair opportunity window.

## Target Gate

`passed`

Reason:

- assimilator attempt/success was recorded
- cybernetics core attempt/success was recorded
- the tech-chain opportunity was fairly exposed in the same valid run

## Stretch Gate

`passed`

Reason:

- first combat-unit production command path appeared without claiming army-core
  success

## What This Proves

- R1 build-chain capability has real evidence
- gateway-ready and early tech-chain opportunity were fairly exposed
- the project can enter army-core implementation work without returning to the
  duration-window contract

## What This Does Not Prove

- this does not validate army presence
- this does not validate `own_army_count > 0`
- this does not validate defend / attack / friendly combat
- command-level combat-unit production is not army-core acceptance
