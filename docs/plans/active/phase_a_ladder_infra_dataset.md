# Phase A: Ladder Infrastructure & Scalable Real-Match Dataset

Status: legacy_historical_reference
Execution authority: no
Superseded by: `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`

Legacy note: retained as historical infrastructure-planning context only. It
must not be used as the current execution authority.

Task queue: `docs/plans/active/phase_a_task_queue.yaml`

Manual trigger: `docs/plans/active/phase_a_manual_trigger.md`

## Goal

Establish a real ladder-like match execution and scalable data-collection base for later gameplay and opponent-modeling work.

This phase is about infrastructure, persistence, and a baseline real-match dataset. It does not require bot strength, but it must produce real data at a scale larger than a smoke test.

## Phase Layers

### Phase A1: Infrastructure Gate

Purpose:

- prove runner, artifact contract, manifest, summary, and package dry-run work;
- run one real single-match probe;
- run a small 4-match real smoke batch;
- compute failure and artifact accounting from smoke output.

A1 is only an infrastructure gate. One probe and four smoke matches cannot close Phase A and cannot be presented as a baseline dataset.

### Phase A2: Baseline Real-Match Dataset V0

Purpose:

- collect a run_id-scoped baseline dataset of 24-48 real matches;
- avoid mixing historical runs into current reports;
- produce dataset manifest and quality report;
- create reusable collection levels for later Phase B/C/D data collection.

Suggested coverage:

- 1-2 maps;
- built-in Terran / Zerg / Protoss opponents;
- Easy / Medium difficulties;
- 2-4 repeats per matchup where feasible.

## Scope

- local-play-bootstrap / AI Arena compatible entrypoint, or an equivalent local ladder-like runner;
- package dry-run;
- multi-match real batch execution;
- dataset manifest;
- replay/result/telemetry persistence;
- crash, timeout, and missing artifact statistics;
- fixed commands for reproducible local evaluation.
- baseline dataset chunks;
- merged dataset manifest;
- dataset quality report;
- scalable collection command/config levels.

## Non-goals

- No new gameplay strategy.
- No build-order implementation.
- No opponent-adaptive behavior work.
- No learning-module integration.
- No claim of ladder competitiveness.

## Files Likely To Change

- `evaluation/runner/`
- `evaluation/metrics/`
- `evaluation/reports/`
- `configs/evaluation/`
- `configs/opponents/`
- `scripts/`
- `docs/commands/`
- package/upload metadata if present

## Verification

- Unit tests for manifest/report logic where appropriate.
- Dry-run for package and command wiring.
- Real single-match probe for single-run chain validation.
- Real 4-match smoke for infrastructure validation.
- Real 24-48 match baseline dataset for Phase A closeout.
- Evidence paths for every real match output directory.

## Real-Match-First Rules

- Unit tests only prove code logic.
- Dry-run only proves orchestration flow.
- A real match is required to prove gameplay behavior.
- Multi-match batch runs are required to prove stability.
- Opponent-pool evaluation is required for meaningful showcase value.
- Reports must separate synthetic evidence, dry evidence, and real match evidence.
- Dry-run conclusions must not be packaged as real capability claims.
- Every real match task must output evidence paths.
- Every task must fit one Plus 5-hour quota window; if scope expands, mark `split_required`.

## Data Scale Strategy

- Probe: 1 match; validates single-match chain only.
- Smoke: 4 matches; validates multi-match runner stability only.
- Baseline V0: 24-48 matches; establishes the baseline real-match dataset.
- Evaluation V1: 50-100 matches; supports capability evaluation.
- Opponent Pool Eval: 100+ matches; supports showcase and research comparisons.
- Training / Learning Dataset: hundreds to thousands of matches; future input for learned opponent model, combat predictor, and imitation modules.

## Done Criteria

- A documented command runs a real multi-match ladder-like batch.
- Each match persists result, replay, telemetry, and metadata or records a structured missing-artifact failure.
- Dataset manifest lists match ids, maps, opponents, configs, status, paths, crash/timeout state, and artifact completeness.
- A1 infrastructure gate report summarizes probe/smoke chain health without claiming dataset sufficiency.
- Baseline V0 includes at least 24 real match attempts, or a documented exception explains why it is below 24.
- Merged baseline dataset manifest lists included runs, excluded historical runs, match count, map/opponent coverage, and artifact completeness.
- Dataset quality report summarizes status distribution, crash rate, timeout rate, replay availability, telemetry coverage, match duration, first scout time if available, and current bot behavior limitations.
- Scalable collection command/config levels exist for smoke, baseline, evaluation, regression, and custom run_id collection.
- Reports explicitly state Phase A does not prove bot strength.

## Stop Conditions

- If runner compatibility requires architecture changes, stop and write an ADR or plan note.
- If real match launch becomes unstable, isolate runtime failure before adding reporting.
- If package expectations are unknown, stop with a checklist instead of inventing compatibility claims.
