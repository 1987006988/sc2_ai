# R7 Strong-Bot World Model Master Plan

Status: active
Updated: 2026-04-26
Role: R7 active frontier master plan
Depends on:

- docs/foundation/04_research_direction/r7_strong_bot_world_model_decision.md
- docs/plans/active/r7_strong_bot_world_model_task_queue.yaml
- docs/experiments/r7_strong_bot_data_protocol.md
- docs/experiments/r7_world_model_evaluation_protocol.md

## Goal

R7 aims to produce a stronger research result than the bounded R6 frontier:

1. acquire and audit a stronger bot or teacher substrate;
2. materialize replay or log data with leakage-safe splits;
3. train an action-conditioned counterfactual macro world model;
4. integrate it into a strong substrate through a bounded macro advisor;
5. validate the result offline, online, and externally;
6. produce a defensible interview-ready evidence pack.

## Why This Is a Higher Bar

R7 is not a simplification. It raises the substrate quality:

1. stronger action surface;
2. stronger strategy carrier;
3. stronger replay source;
4. stronger online and external claim potential.

## Phase Structure

### Phase R7.0: Supersede R6 and Freeze History

Goal:
switch the active frontier from R6 to R7 without changing accepted R0-R5 or
accepted R6 historical results.

### Phase R7.1: Strong Bot Acquisition and Audit

Goal:
obtain and audit at least one strong candidate for substrate, teacher, or
comparator use.

### Phase R7.2: Teacher Data Materialization

Goal:
materialize replay or log data into a leakage-safe teacher dataset and baseline
benchmark.

### Phase R7.3: Counterfactual World Model Training

Goal:
train a scratch-first action-conditioned world model on the teacher benchmark.

### Phase R7.4: Strong-Substrate Online Intervention

Goal:
attach the learned model to a bounded macro advisor on the strong substrate and
run A/B/C evaluation.

### Phase R7.5: External Validation and Closeout

Goal:
validate the learned advisor in an external bot ecosystem and produce a bounded
frontier evidence package.

## Hard Rules

1. do not reopen the frozen core queue;
2. do not continue R6 as if it were still the active frontier queue;
3. do not download or vendor third-party bots before license audit;
4. do not train models before teacher data is materialized;
5. do not use strong-bot raw performance as our contribution;
6. do not claim online success without external evidence;
7. do not let warm-start provenance obscure the main claim.

## Completion Rule

R7 is complete only when `r7_checkpoint_Q_frontier_claim_gate` passes target.
