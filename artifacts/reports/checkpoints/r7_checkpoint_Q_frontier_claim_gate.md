# R7 Checkpoint Q: Frontier Claim Gate

Date: 2026-04-27

## Reviewed Tasks

- `r7_task_016_run_external_bot_ecosystem_validation`
- `r7_task_017_prepare_frontier_interview_evidence_pack`

## Evidence Paths

- `configs/evaluation/r7_external_validation.yaml`
- `docs/experiments/r7_interview_claims_and_deliverables.md`
- `artifacts/reports/r7_external_validation/report.md`
- `artifacts/reports/r7_frontier_closeout/report.md`
- `artifacts/reports/r7_frontier_closeout/results_table.md`
- `artifacts/reports/r7_frontier_closeout/claim_boundary.md`
- `artifacts/reports/r7_frontier_closeout/replay_demo_index.md`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/summary.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/baseline/match_result.json`
- `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/world/match_result.json`

## Gate Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = r7_frontier_goal_reached`

## Why It Passes

1. accepted offline evidence exists through `r7_checkpoint_O`
2. accepted internal online evidence exists through `r7_checkpoint_P`
3. accepted external evidence now exists on one valid downloaded-bot slice
4. a bounded closeout package now maps the frontier claim to exact artifacts

## Why Stretch Fails

1. external evidence is still a single bounded slice
2. no AI Arena house-bot or downloadable-bot robustness bundle exists
3. the current closeout package is interview-ready but not publication-ready

## Claim Boundary

This checkpoint accepts:

1. a bounded R7 frontier claim
2. a scratch-first world-model result with offline, internal, and external support
3. progression to `r7_frontier_goal_reached`

This checkpoint does not accept:

1. broad external generalization
2. AI Arena leaderboard strength
3. non-proxy counterfactual causality

## Invalid Evidence Excluded

1. `external_warpgate_probe` is excluded because the external opponent crashed on unseen ability `4132`
2. historical R6 frontier evidence remains historical context only and is not mixed into the R7 accepted table
3. the downloaded substrate's native strength is not treated as our contribution
