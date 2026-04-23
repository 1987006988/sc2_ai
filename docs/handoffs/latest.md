# Handoff: Phase B-R task_4 Real Duration Window Probe

Date: 2026-04-23

## Executed Task

`task_4_real_duration_window_probe`

Status: completed.

## Validation

- Required level: L3
- Achieved level: L3
- Data source: new real match output
- Real validation status: completed

This task ran one real SC2 local match. It did not tune build logic, did not
validate Gateway/Cyber/production capability, did not run batch evaluation, and
did not execute task 5.

## Evidence

Output directory:

- `data/logs/evaluation/phase_b_revalidation_duration_probe/reallaunch-7d883e41/`

Artifacts:

- `match_result.json`: present
- `match.SC2Replay`: present
- `telemetry/events.jsonl`: present
- `launch_path_diagnostics.json`: present

Key result fields:

- status: `max_game_time_reached`
- result: `Result.Defeat`
- failure_reason: `null`
- exit_reason: `max_game_time_reached`
- runtime_max_game_loop: `7200`
- requested_game_time_limit_seconds: `352`

Telemetry summary:

- event_count: `20508`
- max_game_loop: `7200`
- max_game_time: `321.42857142857144`

## Gate Results

Minimum gate: passed.

- `actual_game_time=321.43s`, which is above the 300s opportunity window.
- Result, replay, and telemetry artifacts exist.

Target gate: passed.

- `match_result.json` records structured status and failure reason.
- Runtime request fields are present in `match_result.json`.
- Telemetry confirms the match reached `game_loop=7200`.

Stretch gate: partial.

- Requested runtime window is visible in `match_result.json`.
- No separate config snapshot artifact was produced.

## What This Proves

- The Phase B-R gameplay runtime window is no longer capped at the old
  `game_time≈116.07` limit.
- The runner and bot config can produce a real match that reaches the >=300s
  opportunity window.
- It is fair to proceed to the build-chain revalidation probe.

## What This Does Not Prove

- It does not validate Gateway-ready, Cyber Core, combat-unit production,
  attack/defend, friendly combat, Level 1, or ladder competitiveness.
- It does not prove any gameplay capability beyond duration-window readiness.

## Blockers

None for task 4.

## Next Pending Task

`task_5_build_chain_revalidation_probe`

Do not execute it until the user explicitly asks to continue the Phase B-R
queue.
