# Handoff: Phase B-R task_3 Checkpoint A

Date: 2026-04-22

## Executed Task

`task_3_checkpoint_A_duration_window_acceptance`

Status: completed.

Decision: `accepted_continue`

Next allowed task: `task_4_real_duration_window_probe`

## Validation

- Required level: L2
- Achieved level: L2
- Data source: dry-run / static config and test evidence
- Real validation status: not applicable for this checkpoint

No SC2 match was run. No gameplay code was changed. Phase C was not started.
The next task was not executed.

## Reviewed Tasks

- `task_1_duration_window_contract`
- `task_2_runtime_window_parameterization`

## Checkpoint Findings

Minimum gate: passed.

- Opportunity-window rules exist.
- `insufficient_duration` is defined as the required classification when
  `actual_game_time < required_min_game_time`.
- Runtime window is configurable through bot config.
- Phase B-R duration probe uses `configs/bot/phase_b_revalidation_gameplay.yaml`
  instead of `configs/bot/debug.yaml`.

Target gate: passed.

- Phase B-R gameplay config sets `runtime.max_game_loop: 7200`.
- The derived python-sc2 `game_time_limit` is 352 seconds.
- `debug.yaml` remains a short-window config with `max_game_loop: 2600` and a
  derived run-game limit of 147 seconds.
- `run_match.py` derives python-sc2 `game_time_limit` from bot
  `runtime.max_game_loop` instead of using fixed 120 seconds.
- Successful real-match result payloads will record:
  - `runtime_max_game_loop`
  - `requested_game_time_limit_seconds`

Stretch gate: partial.

- Expected runtime window is visible in future real match result payloads.
- No standalone metrics/report helper was added.

## Evidence Paths

- `docs/plans/active/phase_b_revalidation_playable_core.md`
- `docs/plans/active/phase_b_revalidation_task_queue.yaml`
- `configs/bot/phase_b_revalidation_gameplay.yaml`
- `configs/evaluation/phase_b_revalidation_duration_probe.yaml`
- `evaluation/runner/run_match.py`
- `tests/unit/test_config_loader.py`
- `tests/integration/test_evaluation_config.py`

## Verification

- `python -m pytest tests/unit/test_config_loader.py tests/integration/test_evaluation_config.py`
  - result: 18 passed
- Queue YAML parse:
  - result: `QUEUE_YAML_OK`
- Runtime window dry check:
  - `configs/bot/debug.yaml 2600 147`
  - `configs/bot/phase_b_revalidation_gameplay.yaml 7200 352`

## What This Proves

- Checkpoint A accepts the duration-window contract and runtime-window
  parameterization.
- It is now valid to proceed to the real duration-window probe in task 4.

## What This Does Not Prove

- It does not prove a real SC2 match reaches 300s.
- It does not prove Gateway ready, Cyber Core, combat-unit production,
  attack/defend, friendly combat, Level 1, or ladder competitiveness.
- It does not validate gameplay capability.

## Blockers

None for checkpoint A.

The next task must provide real SC2 evidence that the new window reaches
`actual_game_time >= 300s` or natural end.

## Next Pending Task

`task_4_real_duration_window_probe`

Do not execute it until the user explicitly asks to continue the Phase B-R
queue.
