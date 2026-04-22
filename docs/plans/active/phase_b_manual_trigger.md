# Phase B Manual Trigger

Status: active.

Queue: `docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml`

Phase: Playable Competitive Core

## Manual Trigger Prompt

Use this prompt when starting the next Phase B task:

```text
Continue Phase B task queue.

Read docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml, find the first task with status pending or in_progress, and execute only that one task.

Rules:
- Do not execute any later task.
- Keep the task within one Plus 5-hour quota window.
- Follow the task scope, non_goals, verification, done_criteria, and stop_conditions.
- If scope expands, stop and mark split_required or blocked.
- If a task requires L3, use real SC2 local match evidence and record evidence_paths.
- If a task is L0/L1/L2, do not run SC2 unless the task explicitly requires it.
- Update docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml and docs/handoffs/latest.md.
- Stop after this one task and report the next pending task.

Real-Match-First:
- Unit tests only prove code logic.
- Dry-run only proves orchestration.
- Real matches prove gameplay behavior.
- Multi-match batches prove stability.
- Reports must distinguish synthetic, dry, and real evidence.
- Do not claim bot strength from dry-run or synthetic evidence.
- Do not claim ladder competitiveness in Phase B.
```

## Validation Levels

- L0: static doc/config exists
- L1: schema/unit/config validation
- L2: dry-run / telemetry dry path / no real SC2
- L3: real SC2 local match gameplay evidence

## Current Queue Start

The next pending task after queue creation is:

- `task_1_build_progression_contract`

## Phase B Closeout Gate

Phase B cannot close unless:

- Gateway real probe reaches L3.
- Assimilator/Cybernetics Core real probe reaches L3.
- Combat-unit production real probe reaches L3.
- Attack/defend order real probe reaches L3.
- Combat event real probe reaches L3, or records a clear structured reason for no combat.
- Phase B small real evaluation reaches L3.
- Phase B report uses real match data.
- Report states whether current data shows wins against built-in Easy/Medium.
- Report does not claim ladder competitiveness.
