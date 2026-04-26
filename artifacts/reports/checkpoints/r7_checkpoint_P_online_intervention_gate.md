# R7 Checkpoint P: Online Intervention Gate

Date: 2026-04-27

## Reviewed Tasks

- `r7_task_013_integrate_world_model_macro_advisor`
- `r7_task_014_run_online_strong_substrate_ablation`

## Evidence Paths

- `configs/evaluation/r7_online_internal.yaml`
- `configs/research/r7_selected_strong_bot.yaml`
- `third_party/strong_bots/sludge-revived/r7_run_eval.py`
- `third_party/strong_bots/sludge-revived/bot/r7/bots.py`
- `third_party/strong_bots/sludge-revived/bot/r7/spending.py`
- `third_party/strong_bots/sludge-revived/bot/r7/macro_advisor.py`
- `third_party/strong_bots/sludge-revived/sc2/paths.py`
- `artifacts/models/r7_world_model/scratch_ensemble_v0_runtime.json`
- `artifacts/reports/r7_online_integration/report.md`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/summary.json`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/baseline/match_result.json`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/rule/match_result.json`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/world/match_result.json`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/world/advisor_stats.json`
- `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/world/match.SC2Replay`

## Gate Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = r7_task_016_run_external_bot_ecosystem_validation`

## Why It Passes

1. Arm A, Arm B, and Arm C all run on the same accepted strong substrate:
   - `sludge_revived_current_patch_house_bot`
2. the learned advisor changes real substrate behavior rather than only emitting tags
3. the accepted online slice shows a directionally positive outcome:
   - Arm A `Tie`
   - Arm B `Tie`
   - Arm C `Victory`
4. the causal behavior delta is explicit:
   - Arm B is locked into `defensive_hold`
   - Arm C mixes `add_tech`, `defensive_hold`, and `increase_production_tempo`
5. accepted evidence is separated from the earlier mis-scoped historical Protoss carrier probe

## Why Stretch Fails

1. accepted evidence is still a single internal slice
2. no multi-map or multi-opponent robustness bundle exists yet
3. no external bot-ecosystem evidence has been accepted yet

## Claim Boundary

This checkpoint accepts:

1. strong-substrate online advisor integration
2. one accepted internal online slice with positive learned outcome
3. progression to external validation

This checkpoint does not accept:

1. external bot support
2. broader online robustness
3. any claim that the downloaded substrate's base strength is our own contribution

## Invalid Evidence Excluded

1. historical executable Protoss carrier artifacts are diagnostic only:
   - `data/logs/evaluation/r7_online_probe/...`
   - `data/logs/evaluation/r7_online_intervention/r7_online_internal_20260427/summary.json`
2. DI-star remains accepted as a teacher source, not as accepted online substrate evidence
3. pre-repair over-expansion probes are not mixed into the accepted table
