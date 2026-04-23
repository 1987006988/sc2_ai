# Handoff: GPT Pro Second-Round Files Imported And Control Layer Switchover Prepared

Date: 2026-04-24

## Scope

This round imported the second-round GPT Pro execution-recipe files from
`docs/pro2.txt`, marked legacy plans as historical-only, and prepared the
research control-layer switchover. No gameplay code was changed. No tests ran.
No SC2 run was started. No Phase A / B / B-R / research queue task was
executed.

## Imported Second-Round Files

- `docs/plans/active/phase_playable_core_rebuild.md`
- `docs/plans/active/phase_adaptive_response_research.md`
- `docs/experiments/checkpoint_acceptance_spec.md`
- `docs/agents/codex_execution_rules_research_mode.md`
- `docs/templates/task_recipe_template.md`
- `docs/experiments/failure_repair_playbook.md`

## Import Status

- missing: none
- partial_imported: none
- second_round_imported: complete

All six target files existed in `docs/pro2.txt` with explicit `文件路径：...`
boundaries and were written to their real paths.

## Active Control Layer

These files are now the current execution authority:

- `docs/foundation/04_research_direction/research_direction_decision.md`
- `docs/foundation/04_research_direction/retain_rewrite_drop_matrix.md`
- `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/experiments/real_match_validation_protocol.md`
- `docs/plans/active/phase_playable_core_rebuild.md`
- `docs/plans/active/phase_adaptive_response_research.md`
- `docs/experiments/checkpoint_acceptance_spec.md`
- `docs/agents/codex_execution_rules_research_mode.md`
- `docs/templates/task_recipe_template.md`
- `docs/experiments/failure_repair_playbook.md`

## Legacy Plans Marked As Historical Reference

- `docs/plans/active/MASTER_PLAN_interview_demo_v0.md`
- `docs/plans/active/ladder_ready_adaptive_sc2_bot_roadmap.md`
- `docs/plans/active/phase_l0_ladder_readiness.md`
- `docs/plans/active/phase_l1_playable_competitive_core.md`
- `docs/plans/active/phase_l2_opponent_adaptive_strategy.md`
- `docs/plans/active/phase_b_playable_competitive_core.md`
- `docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml`
- `docs/plans/active/phase_b_manual_trigger.md`
- `docs/plans/active/phase_b_revalidation_playable_core.md`
- `docs/plans/active/phase_b_revalidation_task_queue.yaml`
- `docs/plans/active/phase_b_revalidation_manual_trigger.md`
- `docs/plans/active/phase_a_ladder_infra_dataset.md`
- `docs/plans/active/phase_a_task_queue.yaml`
- `docs/plans/active/phase_a_manual_trigger.md`

Legacy separation index:

- `docs/plans/legacy_index.md`

## Current Interpretation

The source-of-truth has now been upgraded from candidate first-round drafts to
a complete control layer, because both the first-round and second-round files
are present and imported.

Old plan files remain as historical background only. They must not drive task
selection by themselves.

## Next Step

The next allowed action is to start from:

- `docs/plans/active/research_master_task_queue.yaml`

Old queues are no longer execution entrypoints. New execution must reference the
active control layer above and use the new master queue as the only task source.
