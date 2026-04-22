# Phase 1D Manual Trigger Instructions

## Scheduling Status

There is no real every-6-hour scheduler available in the current Codex tool
environment. Do not claim automated scheduling is active.

Phase 1D uses manual queue triggering. The user should trigger one queue task at
a time, ideally every 6 hours or whenever a new Codex Plus usage window is
available.

## Manual Trigger Prompt

Use this prompt for the next run:

```text
Read docs/plans/active/phase1d_task_queue.yaml and execute exactly the first
pending task according to the queue rules. Do not execute more than one task.
Run only that task's verification. Update docs/plans/active/phase1d_task_queue.yaml
and docs/handoffs/latest.md, then stop.
```

## Required Per-Run Behavior

Each run must:

1. Read `docs/plans/active/phase1d_task_queue.yaml`.
2. Find the first task with `status: in_progress`; if none exists, find the
   first task with `status: pending` whose `requires` entries are all completed.
3. Mark only that task as `in_progress`.
4. Execute only that task's scope.
5. Run only that task's verification.
6. Update the task's validation fields:
   - `actual_validation_level`
   - `data_source`
   - `real_validation_status`
   - `evidence_paths`
7. Mark the task `completed`, `blocked`, or leave `in_progress` with a clear
   continuation note.
8. Update `docs/handoffs/latest.md`.
9. Stop.

## Validation Levels

- `L0`: static/code check. Files, interfaces, or configs exist.
- `L1`: unit test. Synthetic input or fake observation verifies code logic.
- `L2`: dry telemetry. Dry path can write telemetry.
- `L3`: real telemetry. Real SC2 local match contains the target telemetry.

Do not treat a task as real-match validated unless `actual_validation_level` is
`L3`, `data_source` is real match telemetry, and `evidence_paths` records the
real output directory or telemetry file.

## Quota Safety Rules

- Do not continue to another task even if context remains.
- Do not expand task scope to “finish Phase 1D faster.”
- If more than `max_scope_files` are needed, stop and mark `blocked` or
  `split_required` in handoff.
- Real SC2 probe runs are allowed only in tasks that explicitly require `L3`.
- Real SC2 batch runs are split into task 11a through task 11d.
- If verification fails repeatedly, stop and mark the task `blocked`.
- Do not execute task 7 until `task_6b_real_opponent_prediction_telemetry_probe`
  is completed with L3 evidence.
