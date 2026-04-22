# Phase 1E Manual Trigger Instructions

## Scheduling Status

There is no real every-6-hour scheduler available in the current Codex tool
environment. Do not claim automated scheduling is active.

Phase 1E uses manual queue triggering. The user should trigger one queue task at
a time, ideally when a new Codex Plus usage window is available.

## Manual Trigger Prompt

Use this prompt for the next run:

```text
Continue Phase 1E task queue.

Read docs/plans/active/phase1e_task_queue.yaml and execute exactly the first
pending or in_progress task according to the queue rules. Do not execute more
than one task. Run only that task's verification. Update
docs/plans/active/phase1e_task_queue.yaml and docs/handoffs/latest.md, then
stop.
```

## Required Per-Run Behavior

Each run must:

1. Read `docs/plans/active/phase1e_task_queue.yaml`.
2. Find the first task with `status: in_progress`; if none exists, find the
   first task with `status: pending` whose `requires` entries are all completed.
3. Execute only that task.
4. Run only that task's verification.
5. Update the task's validation fields:
   - `actual_validation_level`
   - `data_source`
   - `real_validation_status`
   - `evidence_paths`
6. Mark the task `completed`, `blocked`, or leave `in_progress` with a clear
   continuation note.
7. Update `docs/handoffs/latest.md`.
8. Stop.

## Validation Levels

- `L0`: static/code check. Files, interfaces, or configs exist.
- `L1`: unit test. Synthetic input or fake observation verifies code logic.
- `L2`: dry telemetry. Dry path can write telemetry.
- `L3`: real telemetry. Real SC2 local match contains the target telemetry.

## Quota Safety Rules

- Do not continue to another task even if context remains.
- Do not expand task scope to finish Phase 1E faster.
- If more files or behavior are needed than the task allows, stop and mark the
  task `blocked` or `split_required` in handoff.
- Real SC2 probes are allowed only in tasks that explicitly require L3.
- Real SC2 batch work is isolated to the small ablation task.
- Do not start Phase 1F until `task_11_phase1e_closeout` is completed.
