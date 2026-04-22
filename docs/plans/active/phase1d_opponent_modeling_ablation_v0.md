# Plan: Phase 1D Opponent Modeling Ablation V0

Status: completed on 2026-04-20.

## Summary

Phase 1D creates the first opponent-modeling experiment loop. The work is split
into small tasks that can be executed one at a time within a Codex Plus work
window.

## Key Changes

- Add minimal configurable Protoss supply sustain.
- Add rule-based opponent-model prediction v0.
- Record `opponent_prediction` telemetry for null and rule_based modes.
- Extract fixed telemetry features from real match outputs.
- Run null vs rule_based ablation on a small fixed opponent pool.
- Generate machine-readable `summary.json` and readable `report.md`.

## Verification

- `python -m pytest tests`
- one real match with `opponent_model.mode = null`
- one real match with `opponent_model.mode = rule_based`
- one ablation batch with at least 2 opponents x 2 bot configs
- feature extraction and report generation from real telemetry

Closeout evidence:

- test suite: `python -m pytest tests` -> 35 passed;
- rule-based L3 probe:
  `data/logs/evaluation/phase1d_task6b_probe/reallaunch-f4b16b51/`;
- null L3 match:
  `data/logs/evaluation/phase1d_task11a_null_match/reallaunch-b111cf67/`;
- rule-based L3 match:
  `data/logs/evaluation/phase1d_task11b_rule_based_match/reallaunch-edba8ac0/`;
- real ablation batch:
  `data/logs/evaluation/phase1d_ablation_opponent_model/summary.json`;
- report artifacts:
  `artifacts/reports/phase1d_ablation_opponent_model/summary.json` and
  `artifacts/reports/phase1d_ablation_opponent_model/report.md`.

The ablation is prediction-only. It validates configuration switching,
telemetry, feature extraction, metrics, and reporting. It does not prove that
rule-based opponent modeling improves win rate or gameplay quality.

## Documentation

After Phase 1D completion, update:

- `docs/context/current_status.md`
- `docs/context/validated_findings.md`
- `docs/context/open_hypotheses.md`
- `docs/handoffs/latest.md`
- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`

## Assumptions

- Each queued task is executed independently.
- Do not continue to the next task if the current task is incomplete or blocked.
- Rule-based prediction remains prediction-only until a later milestone.
- Do not expand into SMAC, LLMs, world-model-lite, replay learning, complex build
  orders, army production, or expansion.
