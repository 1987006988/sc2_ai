# Plan: Phase 1D Opponent Modeling Ablation V0

## Status

Completed

## Summary

Establish the first opponent-modeling experiment loop: minimal Protoss supply
sustain, rule-based prediction-only opponent model v0, opponent prediction
telemetry, telemetry feature extraction, and null-vs-rule_based ablation
reporting.

## Key Changes

- Add configurable Protoss pylon sustain to avoid immediate supply stall.
- Keep gameplay behavior independent from opponent-model predictions.
- Record full null and rule-based opponent predictions in telemetry.
- Extract fixed opponent-model features from real match telemetry and result
  files.
- Run a small fixed-pool ablation with null and rule-based bot configs.
- Generate machine-readable `summary.json` and a short markdown report.

## Verification

- `python -m pytest tests`
- one real local match with `opponent_model.mode = null`
- one real local match with `opponent_model.mode = rule_based`
- one real Phase 1D ablation batch with at least two opponents and two bot
  configs
- feature extraction and report generation from real telemetry

## Documentation

Update:

- `docs/context/current_status.md`
- `docs/context/validated_findings.md`
- `docs/context/open_hypotheses.md`
- `docs/handoffs/latest.md`
- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`

Add a lesson only if implementation uncovers a reusable pitfall.

## Assumptions

- Supply sustain is Protoss-only in Phase 1D.
- The rule-based opponent model is prediction-only and must not alter gameplay.
- The ablation report proves the experiment loop and telemetry chain, not win
  rate improvement.
- The first real ablation can use one map and two or more built-in opponents to
  keep runtime short.
