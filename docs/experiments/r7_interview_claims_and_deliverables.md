# R7 Interview Claims And Deliverables

Status: active
Updated: 2026-04-27
Role: defines the bounded R7 claim and the minimum closeout package.

## Allowed Top-Line Claim

Only after `r7_checkpoint_Q_frontier_claim_gate` passes, the project may claim:

1. a strong-bot-anchored macro world-model line exists;
2. the learned world-model is trained on a teacher dataset rather than copied
   from the downloaded substrate;
3. the learned advisor changes macro behavior on the accepted strong substrate;
4. offline, internal, and external evidence all exist.

## Disallowed Overclaim

Do not claim:

1. AI Arena top-bot level;
2. broad external generalization;
3. full counterfactual causality beyond the current proxy supervision;
4. the downloaded substrate's raw strength as our own contribution.

## Minimum Deliverables

1. `artifacts/reports/r7_world_model_training/report.md`
2. `artifacts/reports/r7_online_integration/report.md`
3. `artifacts/reports/r7_external_validation/report.md`
4. `artifacts/reports/r7_frontier_closeout/report.md`
5. `artifacts/reports/r7_frontier_closeout/results_table.md`
6. `artifacts/reports/r7_frontier_closeout/claim_boundary.md`
7. `artifacts/reports/r7_frontier_closeout/replay_demo_index.md`

## Evidence Mapping Rule

Every top-line claim in the closeout package must point to:

1. one accepted offline artifact;
2. one accepted internal online artifact;
3. one accepted external artifact;
4. any invalid or diagnostic runs that were explicitly excluded.
