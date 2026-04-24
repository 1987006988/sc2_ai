# Legacy Plan Status Index

Status: active_index
Purpose: separate the current active control layer from legacy historical plans.

## Active Control Layer

These files are the current execution authority:

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

## Legacy Strategy / Roadmap Docs

- `docs/plans/active/MASTER_PLAN_interview_demo_v0.md`
- `docs/plans/active/ladder_ready_adaptive_sc2_bot_roadmap.md`
- `docs/plans/active/phase_l0_ladder_readiness.md`
- `docs/plans/active/phase_l1_playable_competitive_core.md`
- `docs/plans/active/phase_l2_opponent_adaptive_strategy.md`

Why retained:

- they show how project framing evolved over time.

What they can still tell us:

- prior roadmap intent;
- previous milestone naming;
- how the project moved from demo framing to research-control governance.

What they can no longer decide:

- current execution priority;
- current task selection;
- acceptance authority.

## Legacy Phase Plans

- `docs/plans/active/phase_b_playable_competitive_core.md`
- `docs/plans/active/phase_b_revalidation_playable_core.md`
- `docs/plans/active/phase_a_ladder_infra_dataset.md`

Why retained:

- they preserve the detailed context behind accepted infrastructure work and
  non-accepted playable-core work.

What they can still tell us:

- what was attempted;
- what evidence existed;
- where capability validation failed or was downgraded.

What they can no longer decide:

- whether those phases are active now;
- whether the old phase conclusions are still authoritative;
- what the next task should be.

## Legacy Queues / Manual Triggers

- `docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml`
- `docs/plans/active/phase_b_manual_trigger.md`
- `docs/plans/active/phase_b_revalidation_task_queue.yaml`
- `docs/plans/active/phase_b_revalidation_manual_trigger.md`
- `docs/plans/active/phase_a_task_queue.yaml`
- `docs/plans/active/phase_a_manual_trigger.md`

Why retained:

- they preserve prior queue structure, gating logic, and execution history.

What they can still tell us:

- which tasks were attempted;
- how earlier validation logic was structured;
- what legacy manual prompts looked like.

What they can no longer decide:

- the current execution entrypoint;
- the current active task;
- whether work may continue from those queues.

## Retained Diagnostic Evidence Docs

Examples include:

- Phase A infrastructure/data foundation reports
- Phase B evidence audit reports
- Phase 1D / Phase 1E telemetry and ablation reports

Why retained:

- they provide real-match provenance, audit trails, and failure-class history.

What they can still tell us:

- what was validated historically;
- what was only diagnostic;
- which blockers were real versus tooling/config artifacts.

What they can no longer decide:

- the current task source;
- whether a historical phase is active again;
- whether a historical `completed` result should be treated as current success.

Use the active control layer above to decide what to execute next.
