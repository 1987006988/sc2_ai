# Validated Findings

## 2026-04-17: Phase-1 engineering base defaults to bare python-sc2

Evidence:

- import checks for `sc2` and `ares` in the current environment returned missing;
- dry-run package resolution attempts for `sc2` and `ares-sc2` did not resolve usable packages in the current environment;
- the project already maintains its own runtime and manager boundaries.

Conclusion:

- phase 1 should target bare python-sc2 as the engineering base;
- Ares-sc2 is not required to begin phase-1 implementation.

## 2026-04-17: Local evaluation skeleton now persists match results

Evidence:

- `scripts/dev/run_smoke_eval.ps1`
- `data/logs/evaluation/smoke/summary.json`

Conclusion:

- the project now has a minimal local dry-run evaluation loop that saves match results and replay metadata placeholders.

## 2026-04-17: Project now supports SC2PATH-based runtime preflight

Evidence:

- local root path verified at `D:\games\StarCraft II`
- `scripts/setup/check_env.ps1`
- `tests/unit/test_sc2_installation.py`

Conclusion:

- runtime and evaluation now resolve SC2 from the `SC2PATH` environment variable;
- required installation structure is checked before real launch;
- real-launch mode can fail loudly and persist the failure reason.

## 2026-04-17: Real SC2 process launch validation works on this machine

Evidence:

- `SC2PATH=D:\games\StarCraft II`
- `scripts/setup/check_env.ps1`
- local real-launch probe under `data/logs/evaluation/real_launch_probe/`

Conclusion:

- the project can now launch the real `StarCraft II.exe` process and terminate it after timeout for validation;
- process-launch validation is working;
- full match orchestration is still a separate next step.

## 2026-04-17: AI Arena ladder-test maps are installed in the local SC2 Maps root

Evidence:

- `D:\games\StarCraft II\Maps`
- `IncorporealAIE_v4.SC2Map`
- `LeyLinesAIE_v3.SC2Map`

Conclusion:

- the local machine now has a real SC2 `Maps` directory;
- phase-1 evaluation config can point at real installed map entries instead of placeholders.

## 2026-04-17: Real python-sc2-backed local match entry now works in this repository

Evidence:

- `burnysc2==7.2.1` installed locally
- real probe under `data/logs/evaluation/real_local_probe/`
- replay saved as `match.SC2Replay`

Conclusion:

- the project can now initiate a real local SC2 match through python-sc2 on a real installed map;
- telemetry, match result, and replay metadata all persist through the project runner;
- the remaining gap is gameplay depth, not runtime-path discovery.

## 2026-04-20: Real local bot loop no longer exits after one probe step

Evidence:

- `src/sc2bot/runtime/game_loop.py`
- `tests/unit/test_game_loop.py`
- `python -m pytest tests/unit`
- `python -m pytest tests/integration/test_bot_startup.py tests/integration/test_evaluation_config.py`
- Windows PowerShell real launch from WSL with `SC2PATH=D:\games\StarCraft II`
- `data/logs/evaluation/windows_real_launch_probe/reallaunch-9c0ca256/`

Conclusion:

- the python-sc2 local bot now runs the existing manager pipeline until a sustained `game_loop` limit;
- the exit event is telemetry-labeled as a sustained runtime limit, not as a one-step probe exit;
- real validation reached `game_loop=2600`, wrote `sc2_match_sustain_limit_reached`, saved `match.SC2Replay`, and persisted `Result.Defeat`;
- this validates runtime continuity only and does not add gameplay strategy.

## 2026-04-20: Phase 1C survival baseline produces live opponent observations

Evidence:

- `python -m pytest tests`
- single real match: `data/logs/evaluation/phase1c_single_real/reallaunch-64588eb0/`
- real batch: `data/logs/evaluation/phase1c_real_smoke/summary.json`
- latest batch match ids: `reallaunch-908b50f7`, `reallaunch-8e19a96e`, `reallaunch-db482309`, `reallaunch-76d0c874`

Conclusion:

- the bot now records enriched `game_state` and `scouting_observation` telemetry from live python-sc2 observations;
- the worker scout produced non-empty enemy observations including enemy workers, combat units, and structures;
- `opponent_model_mode` is recorded in runtime telemetry;
- the small built-in opponent pool ran through real SC2 with independent result directories and replay files;
- every latest batch match exited with `max_game_time_reached`, not a probe exit.

## 2026-04-20: Phase 1D opponent-modeling ablation v0 is established

Evidence:

- `python -m pytest tests`
- null real match: `data/logs/evaluation/phase1d_single_null/reallaunch-22e80b36/`
- rule-based real match: `data/logs/evaluation/phase1d_single_rule_based/reallaunch-b1f5139f/`
- ablation batch: `data/logs/evaluation/phase1d_ablation_opponent_model/summary.json`
- report: `artifacts/reports/phase1d_ablation_opponent_model/report.md`

Conclusion:

- Protoss supply sustain can issue pylon build commands and records attempt/success/skip telemetry;
- null and rule-based modes both emit `opponent_prediction` telemetry;
- rule-based prediction v0 produces risk signals from live scouting observations;
- feature extraction handles real telemetry and writes fixed fields for ablation analysis;
- the generated report explicitly treats the experiment as prediction-only and does not claim win-rate improvement.

## 2026-04-20: task_6b real opponent-prediction telemetry probe reached L3

Evidence:

- real local match output: `data/logs/evaluation/phase1d_task6b_probe/reallaunch-f4b16b51/`
- `match_result.json`
- `match.SC2Replay`
- `telemetry/events.jsonl`
- match status: `max_game_time_reached`
- bot config: `configs/bot/opponent_model_rule_based.yaml`

Conclusion:

- a real SC2 local match with `opponent_model.mode = rule_based` wrote
  `opponent_prediction` telemetry;
- the event payload includes `opponent_model_mode` and serialized prediction
  fields including `prediction_mode`, `signals`, `rush_risk`, `tech_risk`, and
  `confidence`;
- this validates the opponent-prediction telemetry path at L3 for task 6b;
- feature extraction can now use this real match directory as its required
  acceptance input.

## 2026-04-20: Phase 1D closeout reached L3 real ablation reporting

Evidence:

- `python -m pytest tests` -> 35 passed;
- rule-based real telemetry probe:
  `data/logs/evaluation/phase1d_task6b_probe/reallaunch-f4b16b51/`;
- null real match:
  `data/logs/evaluation/phase1d_task11a_null_match/reallaunch-b111cf67/`;
- rule-based real match:
  `data/logs/evaluation/phase1d_task11b_rule_based_match/reallaunch-edba8ac0/`;
- real 2x2 ablation batch:
  `data/logs/evaluation/phase1d_ablation_opponent_model/summary.json`;
- generated report artifacts:
  `artifacts/reports/phase1d_ablation_opponent_model/summary.json` and
  `artifacts/reports/phase1d_ablation_opponent_model/report.md`.

Conclusion:

- the first prediction-only opponent-modeling experiment loop is complete;
- null and rule-based modes both emit real `opponent_prediction` telemetry;
- feature extraction, metrics summary, and Markdown reporting work on real
  match outputs;
- the result validates the telemetry and reporting chain only;
- it does not prove win-rate, gameplay-quality, or strategy-improvement gains
  because rule-based predictions still do not affect gameplay behavior.

## 2026-04-21: Phase 1E minimal strategy intervention reached L3 real reporting

Evidence:

- `python -m pytest tests` -> 49 passed;
- tag-only real telemetry probe:
  `data/logs/evaluation/phase1e_task5_tag_only_probe/reallaunch-350f1ad9/`;
- minimal_behavior real telemetry probe:
  `data/logs/evaluation/phase1e_task7_minimal_behavior_probe/reallaunch-0997c3b4/`;
- real 1 map x 2 opponents x 3 configs ablation:
  `data/logs/evaluation/phase1e_strategy_intervention_ablation/20260421T145911Z/`;
- generated report artifacts:
  `artifacts/reports/phase1e_strategy_intervention/summary.json` and
  `artifacts/reports/phase1e_strategy_intervention/report.md`.

Conclusion:

- rule-based predictions can be converted into `selected_response_tag` and
  `strategy_switch_reason`;
- tag-only mode records real `strategy_response` and `strategy_switch`
  telemetry without behavior intervention;
- minimal_behavior mode records real `minimal_behavior_intervention` telemetry;
- the small real ablation compares `null`, `rule_based_prediction_only`, and
  `minimal_behavior` configs on a fixed local pool;
- the report validates telemetry and reporting paths only;
- it does not prove win-rate or gameplay-quality improvement.

## 2026-04-21: Phase 1D/1E are foundation, not final ladder capability

Evidence:

- Phase 1D report artifacts exist under
  `artifacts/reports/phase1d_ablation_opponent_model/`;
- Phase 1E report artifacts exist under
  `artifacts/reports/phase1e_strategy_intervention/`;
- current runtime can launch real local SC2 matches and persist replay, result,
  telemetry, and report artifacts;

## 2026-04-22: Phase A real-match dataset foundation reached closeout

Evidence:

- A1 infrastructure report:
  `artifacts/reports/phase_a_ladder_infra_dataset/a1_infrastructure_gate/summary.json`;
- merged Baseline Dataset V0 manifest:
  `data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json`;
- dataset quality report:
  `artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/summary.json`
  and `artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/report.md`;
- reusable collection levels:
  `configs/evaluation/phase_a_collection_levels.yaml`;
- dry/config evidence for scalable collection:
  `data/logs/evaluation/phase_a_collections/smoke/phase_a_collection_smoke_dry_example/summary.json`.

Conclusion:

- Phase A established infrastructure and data-foundation evidence for later
  ladder-competitive work;
- Baseline Dataset V0 contains 24 real match attempts;
- coverage includes `incorporeal_aie_v4` and `leylines_aie_v3`;
- opponent coverage includes Terran, Zerg, and Protoss built-in opponents at
  Easy and Medium difficulties;
- every Baseline V0 match has `match_result.json`, `match.SC2Replay`, and
  `telemetry/events.jsonl`;
- dataset quality report shows `crash_rate = 0.0`, `timeout_rate = 0.0`,
  `replay_availability = 1.0`, and `telemetry_availability = 1.0`;
- core telemetry events appear in all 24 matches;
- this validates infrastructure, scoped dataset collection, artifact
  persistence, and reporting only;
- it does not prove bot strength, gameplay quality, ladder competitiveness, or
  win-rate improvement.
- current gameplay still lacks stable build progression, combat production,
  attack/defend behavior, ladder-like package checks, and repeated ladder-style
  stability reporting.

Conclusion:

- Phase 1D/1E validate runtime, telemetry, opponent prediction,
  strategy-response telemetry, reporting, and L3 validation mechanics;
- they do not validate ladder readiness, stable win rate, gameplay quality, or
  opponent-model-driven match improvement;
- Phase 1F demo packaging is paused;
- the active route is now the Ladder-Ready Adaptive SC2 Bot Roadmap, beginning
  with Phase L0 Ladder Readiness.

## 2026-04-22: project goal raised to ladder-competitive adaptive bot

Evidence:

- previous roadmap treated ladder readiness as the next active route;
- current project objective requires repeated ladder-like bot-vs-bot evaluation,
  baseline wins, and opponent-model-driven behavior validation;
- existing Phase 1D/1E evidence validates foundation mechanics but not
  competitiveness or outcome improvement.

Conclusion:

- the active roadmap is now
  `docs/plans/active/ladder_competitive_adaptive_sc2_bot_plan.md`;
- the older Ladder-Ready roadmap is superseded / integrated, not deleted;
- each smallest Codex task should be quota-safe for one Plus 5-hour window, but
  the full project goal should remain ambitious;
- Phase A should create the real match dataset and ladder-like infrastructure
  before gameplay strength claims are attempted;
- reports must follow Real-Match-First evidence discipline.

## 2026-04-22: Phase B real small evaluation completed but Level 1 playable baseline is not reached

Evidence:

- Phase B report:
  `artifacts/reports/phase_b_playable_competitive_core/report.md`;
- Phase B summary:
  `artifacts/reports/phase_b_playable_competitive_core/summary.json`;
- source real small-eval run:
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`;
- source metrics:
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/phase_b_small_eval_metrics.json`;
- 8 real SC2 local matches against built-in Easy Terran, Easy Zerg,
  Easy Protoss, and Medium Terran, with 2 repeats each.

Conclusion:

- Phase B validated real local multi-match execution for the playable-core
  workstream;
- all 8 matches persisted `match_result.json`, `match.SC2Replay`, and
  `telemetry/events.jsonl`;
- Gateway build commands succeeded in all 8 matches;
- army-order telemetry and combat-signal telemetry appeared in real match
  output;
- the report correctly records `level_1_playable_baseline_reached = false`;
- no combat-unit production succeeded in the 8-match eval;
- no telemetry event reported `own_army_count > 0`;
- no `attack_order` appeared;
- all 8 matches ended as `Result.Defeat`;
- Phase B therefore does not prove combat capability, wins against built-in
  Easy/Medium, gameplay quality, or ladder competitiveness.

## 2026-04-22: Phase B evidence audit reclassified task completion vs capability validation

Evidence:

- audit report:
  `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`;
- audited real probes:
  - `data/logs/evaluation/phase_b_task4_gateway_probe/reallaunch-05627d9a/`;
  - `data/logs/evaluation/phase_b_task6_cyber_core_probe/reallaunch-619366ed/`;
  - `data/logs/evaluation/phase_b_task8_combat_unit_probe/reallaunch-1aaf5fc8/`;
  - `data/logs/evaluation/phase_b_task10_attack_defend_probe/reallaunch-fe78a347/`;
  - `data/logs/evaluation/phase_b_task12_combat_event_probe/reallaunch-e73a3d90/`;
  - `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`;
- all audited probes and small-eval matches ended around `game_time=116.07`
  with `status=max_game_time_reached`;
- cutoff source is bot self-exit in `src/sc2bot/runtime/game_loop.py`,
  controlled by `configs/bot/debug.yaml` with `runtime.max_game_loop: 2600`.

Conclusion:

- there was a real acceptance issue: task `completed` had been too easy to
  read as gameplay capability validated;
- Gateway command telemetry is partially validated, but Gateway-ready,
  Assimilator/Cyber Core, combat-unit production, real army orders, and
  friendly combat are not validated;
- primary failure class for post-Gateway capability tasks is
  `insufficient_duration`;
- structured failure reasons and no-army telemetry are useful diagnostics, not
  capability success;
- Phase B is not accepted as a playable competitive core and should not enter
  Phase C before a duration-window fix and rerun of the L3 gameplay probes.
