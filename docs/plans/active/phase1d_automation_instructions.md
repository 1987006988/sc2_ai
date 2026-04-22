# Phase 1D Automation Instructions

## Purpose

Run Phase 1D as a sequence of small Codex tasks. Each automatic or manual run
must execute exactly one task from `phase1d_task_queue.yaml`, then stop.

## Per-Run Procedure

Every run must:

1. Read `docs/plans/active/phase1d_task_queue.yaml`.
2. Find the first task with `status: pending`.
3. Mark that task as `in_progress`.
4. Execute only that task's scope.
5. Run only that task's listed verification, plus any directly required narrow
   checks.
6. If verification succeeds, mark the task `completed`.
7. If implementation or verification fails, mark the task `blocked` and record
   the blocker in `docs/handoffs/latest.md`.
8. Update `docs/handoffs/latest.md` with:
   - task id;
   - status;
   - files changed;
   - verification commands and results;
   - blocker or next continuation point.
9. Stop. Do not execute the next task in the same run.

## Runtime Limit

Each task has `max_runtime_minutes`.

If the current task exceeds its limit:

- stop work;
- save a concise current-change summary in `docs/handoffs/latest.md`;
- mark the task `blocked` if there is a concrete blocker, otherwise leave it
  `in_progress`;
- write the exact continuation point;
- do not continue trying and do not start the next task.

## Stop Conditions

Stop the automation loop when:

- all tasks are `completed`;
- any task is `blocked`;
- verification repeatedly fails;
- the task would require scope expansion beyond its `scope`;
- the task would violate forbidden scope:
  - SMAC;
  - LLM replay summary;
  - world-model-lite;
  - replay imitation learning;
  - complex build order;
  - army production;
  - expansion.

## Scheduling

The current Codex tool environment does not expose a real scheduler for
every-6-hour autonomous execution. Do not claim a timer has been installed.

Manual trigger prompt for the next run:

```text
Read docs/plans/active/phase1d_task_queue.yaml and execute exactly the first
pending task according to docs/plans/active/phase1d_automation_instructions.md.
Do not execute more than one task. Stop after updating docs/handoffs/latest.md.
```

Recommended cadence: run the prompt every 6 hours until all tasks complete or a
task becomes blocked.
