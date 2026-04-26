# sc2-ai

Layered hybrid full-game StarCraft II bot project.

## Goal

The accepted core project goal has already been reached:

1. a Level 1 playable baseline was accepted;
2. one adaptive research contribution was accepted on top of that baseline.

The active frontier goal is now R7:

build a strong-bot-anchored counterfactual macro world model rather than keep
stacking belief gates on the weak self-built baseline.

## Current State

What is true now:

1. `checkpoint_E_level1_baseline_gate` passed;
2. `checkpoint_F_adaptive_research_gate` passed;
3. the frozen core queue ends at `project_core_goal_reached`;
4. R6 completed as a bounded historical frontier result;
5. R7 is now the active frontier queue.

What is not true now:

1. no strong bot has been acquired or audited yet for R7;
2. no R7 teacher dataset has been materialized yet;
3. no R7 world model has been trained yet;
4. no R7 online or external claim exists yet.

## Active Control Layers

Frozen accepted core history:

- `docs/plans/active/research_master_task_queue.yaml`

Active frontier extension:

- `docs/foundation/04_research_direction/r7_strong_bot_world_model_decision.md`
- `docs/plans/active/R7_STRONG_BOT_WORLD_MODEL_MASTER_PLAN.md`
- `docs/plans/active/r7_strong_bot_world_model_task_queue.yaml`
- `docs/experiments/r7_strong_bot_data_protocol.md`
- `docs/experiments/r7_world_model_evaluation_protocol.md`

## Next Step

If execution resumes, it should start from:

- `r7_task_002_identify_and_rank_strong_bot_candidates`

Do not resume the R6 queue as active work.
Do not reopen the frozen core queue.
