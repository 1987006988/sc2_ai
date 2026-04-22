# Phase A1 Infrastructure Gate Report

- Run id: `phase_a_a1_infrastructure_gate`
- Evidence type: `real_infrastructure_gate`
- Probe match count: `1`
- Smoke match count: `4`
- Smoke status counts: `{'max_game_time_reached': 4}`
- Smoke crash rate: `0.0`
- Smoke timeout rate: `0.0`
- Smoke artifact completeness rate: `1.0`

## Evidence

- Probe manifest: `data/logs/evaluation/phase_a_task4_single_probe/dataset_manifest.json`
- Smoke manifest: `data/logs/evaluation/phase_a_real_smoke/phase_a_task5_real_smoke/dataset_manifest.json`
- Failure accounting: `data/logs/evaluation/phase_a_real_smoke/phase_a_task5_real_smoke/failure_accounting_summary.json`

## Interpretation

- The single probe validates the one-match real artifact chain.
- The four-match smoke validates short multi-match orchestration and artifact persistence.
- This is infrastructure evidence only.
- One probe plus four smoke matches do not constitute a baseline dataset.
- Phase A2 baseline dataset collection is still required before Phase A closeout.
- This report does not prove bot strength, ladder competitiveness, or gameplay quality.

## Real-Match-First Classification

- Probe evidence: real match evidence.
- Smoke evidence: real multi-match evidence.
- Capability claim: infrastructure gate only.
