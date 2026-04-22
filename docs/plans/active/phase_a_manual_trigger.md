# Phase A Manual Trigger

Status: active.

Queue: `docs/plans/active/phase_a_task_queue.yaml`

Phase: Ladder Infrastructure & Scalable Real-Match Dataset

## Manual Trigger Prompt

Use this prompt when starting the next Phase A task:

```text
Continue Phase A task queue.

Read docs/plans/active/phase_a_task_queue.yaml, find the first task with status pending or in_progress, and execute only that one task.

Rules:
- Do not execute any later task.
- Keep the task within one Plus 5-hour quota window.
- Follow the task scope, non_goals, verification, done_criteria, and stop_conditions.
- If scope expands, stop and mark split_required or blocked.
- If a task requires L3, use real SC2 local match evidence and record evidence_paths.
- If a task is L0/L1/L2, do not run SC2 unless the task explicitly requires it.
- Update docs/plans/active/phase_a_task_queue.yaml and docs/handoffs/latest.md.
- Stop after this one task and report the next pending task.

Do not write gameplay code unless the active task explicitly says so.
Do not claim bot strength from dry-run or synthetic evidence.
```

## Real-Match-First Rules

1. Unit tests only prove code logic.
2. Dry-run only proves orchestration flow.
3. Real match evidence is required to prove gameplay behavior.
4. Multi-match batch evidence is required to prove stability.
5. Opponent-pool evaluation is required for meaningful showcase value.
6. Reports must distinguish:
   - synthetic evidence;
   - dry evidence;
   - real match evidence.
7. Dry-run conclusions must not be packaged as real capability claims.
8. Every real match task must output evidence paths.
9. Every task must fit one Plus 5-hour quota window; if scope expands, mark `split_required`.

## Validation Levels

- L0: static doc/config exists
- L1: schema/unit/config validation
- L2: dry-run / package dry-run / no real SC2
- L3: real SC2 local match evidence

## Current Queue Start

The next pending task after queue creation is:

- `task_1_real_match_artifact_contract`

## Phase A Layers

### A1 Infrastructure Gate

A1 proves runner, artifact contract, manifest, package dry-run, single real probe, 4-match smoke, and failure accounting work.

A1 is not a baseline dataset and cannot close Phase A.

### A2 Baseline Real-Match Dataset V0

A2 collects a versioned baseline real-match dataset with enough scale to support later Phase B/C/D work.

Target scale:

- 24-48 real matches;
- 1-2 maps;
- built-in Terran / Zerg / Protoss;
- Easy / Medium difficulties;
- 2-4 repeats per matchup where feasible;
- run_id scoped;
- historical runs excluded unless explicitly listed.

## Data Scale Strategy

- Probe: 1 match; validates single-match chain only.
- Smoke: 4 matches; validates multi-match runner stability only.
- Baseline V0: 24-48 matches; establishes the baseline real-match dataset.
- Evaluation V1: 50-100 matches; supports capability evaluation.
- Opponent Pool Eval: 100+ matches; supports showcase and research comparisons.
- Training / Learning Dataset: hundreds to thousands of matches; future input for learned opponent model, combat predictor, and imitation modules.

## Phase A Closeout Gate

Phase A cannot close unless:

- A1 infrastructure gate is complete;
- `task_4_real_single_match_probe` reaches L3;
- `task_5_real_multi_match_smoke` reaches L3;
- `task_6_failure_accounting_summary` uses task_5 real match output;
- baseline dataset has at least 24 real matches, or a documented exception explains why it is below 24;
- `task_8e_merge_baseline_dataset_manifest` uses real baseline chunk outputs;
- `task_8f_dataset_quality_report` uses real baseline dataset outputs;
- `task_8g_scalable_collection_command` is complete;
- reports do not use dry-run or 4-match smoke output as a substitute for baseline real-match evidence;
- reports explicitly state Phase A does not prove bot strength.
