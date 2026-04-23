# Phase B-R Manual Trigger

Status: legacy_historical_reference
Execution authority: no
Superseded by: `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`

Use this file when manually continuing Phase B-R:
`docs/plans/active/phase_b_revalidation_task_queue.yaml`

## Execution Rule

Each manual run executes exactly one task:

1. Read `docs/plans/active/phase_b_revalidation_task_queue.yaml`.
2. Find the first task with `status: pending` or `status: in_progress`.
3. Check all `requires` entries.
4. If requirements are missing, mark the task `blocked` and stop.
5. Execute only that task.
6. Run only the task's own verification.
7. Update the queue and `docs/handoffs/latest.md`.
8. Stop.

Do not execute the next task in the same run.

## Checkpoint Rule

Every third task is a checkpoint. Checkpoints are mandatory gates:

- `task_3_checkpoint_A_duration_window_acceptance`
- `task_6_checkpoint_B_build_chain_acceptance`
- `task_9_checkpoint_C_production_acceptance`
- `task_12_checkpoint_D_tactical_acceptance`
- `task_15_checkpoint_E_phase_b_acceptance`

If a checkpoint decision is not `accepted_continue`, do not run the next group.
Create or request a repair task instead.

## Evidence Rules

1. Unit tests prove code logic only.
2. Dry-run proves orchestration only.
3. Capability tasks require real SC2 match evidence.
4. `completed` does not mean `accepted`.
5. `diagnostic completed` does not mean `capability validated`.
6. Structured failure reasons can complete a diagnostic task, but they cannot
   count as capability success unless a checkpoint explicitly says so.
7. If `actual_game_time < required_min_game_time`, classify capability result
   as `insufficient_duration`.
8. Every task must fit one Plus 5-hour quota window.
9. The total project goal is not downgraded to the minimum gate.

## Forbidden Scope

Unless the current task explicitly permits it:

- no expansion strategy;
- no advanced tech beyond the minimum Cybernetics Core path;
- no upgrades;
- no complex army composition;
- no SMAC;
- no LLM;
- no replay learning;
- no learned opponent model;
- no combat predictor;
- no league/self-play;
- no Phase C work;
- no ladder-competitiveness claim.

## Prompt Template

```text
Continue Phase B-R task queue.

Read docs/plans/active/phase_b_revalidation_task_queue.yaml.
Find the first pending or in_progress task and execute only that task.
Respect requires, scope, non_goals, verification, minimum_gate, target_gate,
stretch_gate, and stop_conditions.
If the task is a checkpoint and decision is not accepted_continue, stop and do
not execute the next group.
Update the queue and docs/handoffs/latest.md.
Do not run SC2 unless this task requires L3 real match evidence.
Do not write gameplay code unless this task explicitly permits it.
Do not enter Phase C.
```
