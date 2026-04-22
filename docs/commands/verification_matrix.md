# Verification Matrix

## Config-only change

Run:

```powershell
python -m pytest tests/unit/test_config_loader.py
```

## Opponent model interface change

Run:

```powershell
python -m pytest tests/unit/test_opponent_model_interface.py tests/unit/test_feature_extractor.py
```

## Live observation / scouting change

Run:

```powershell
python -m pytest tests/unit/test_game_state.py tests/unit/test_scouting_manager.py
```

## Telemetry schema change

Run:

```powershell
python -m pytest tests/unit/test_telemetry_schema.py
```

## Bot startup path change

Run:

```powershell
python -m pytest tests/integration/test_bot_startup.py
scripts/dev/run_bot_local.ps1
```

## SC2 runtime / launch-path change

Run:

```powershell
$env:SC2PATH = "D:\games\StarCraft II"
scripts/setup/check_env.ps1
python -m pytest tests/unit/test_sc2_installation.py
python -m pytest tests/integration/test_evaluation_config.py
```

Expected:

- preflight passes;
- dry-run branch still passes tests;
- real-launch failure reasons are persisted when SC2PATH is invalid;
- on a configured machine, real-launch probe can start a real local SC2 match;
- a replay file is saved for the real-launch probe.
- telemetry contains `game_state`, `scouting_observation`, and `opponent_model_mode`.

## Phase 1C real smoke batch

Run from Windows PowerShell:

```powershell
$repo = "\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai"
Set-Location $repo
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python evaluation/runner/run_batch.py --config configs/evaluation/phase1c_real_smoke.yaml
```

Expected:

- at least two built-in opponents run;
- every match has an independent result directory;
- `summary.json` includes map, opponent, status, duration, failure reason, and replay path;
- telemetry includes non-empty enemy observations when the worker scout reaches the opponent.

## Phase 1D opponent-model ablation

### L3 opponent-prediction telemetry probe

Run from Windows PowerShell:

```powershell
$repo = "\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai"
Set-Location $repo
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
@'
from evaluation.runner.run_match import MatchRequest, run_match
print(run_match(MatchRequest(
    bot_config='configs/bot/opponent_model_rule_based.yaml',
    bot_config_id='rule_based',
    bot_config_tags=('phase1d', 'task6b', 'rule_based'),
    map_id='incorporeal_aie_v4',
    map_name='IncorporealAIE_v4',
    map_file='IncorporealAIE_v4.SC2Map',
    opponent_id='builtin_easy_terran',
    opponent_type='computer',
    opponent_race='terran',
    opponent_difficulty='easy',
    opponent_tags=('builtin', 'easy', 'terran'),
    output_dir='data/logs/evaluation/phase1d_task6b_probe',
    launch_mode='real_launch',
)))
'@ | python -
```

Expected:

- one real local match output directory is created;
- `telemetry/events.jsonl` exists;
- at least one event has `event_type = opponent_prediction`;
- the payload includes `opponent_model_mode`, `prediction`, `prediction_mode`,
  `signals`, `rush_risk`, `tech_risk`, and `confidence`.

### Real ablation batch

Run from Windows PowerShell:

```powershell
$repo = "\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai"
Set-Location $repo
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python evaluation/runner/run_batch.py --config configs/evaluation/phase1d_ablation_opponent_model.yaml
python -m evaluation.reports.run_opponent_model_ablation_report `
  --evaluation-dir data/logs/evaluation/phase1d_ablation_opponent_model `
  --output-dir artifacts/reports/phase1d_ablation_opponent_model
```

Expected:

- at least 2 opponents x 2 bot configs run;
- null and rule-based matches both write `opponent_prediction` telemetry;
- supply sustain telemetry includes attempt/success/skip or failure reasons;
- report summary and markdown are generated;
- report states prediction-only limitations and does not claim win-rate improvement.
- if reusing the same output root, historical match directories may remain in
  the report input; use a fresh output root for clean one-run accounting.

### Phase 1D closeout

Run:

```powershell
python -m pytest tests
Test-Path artifacts/reports/phase1d_ablation_opponent_model/summary.json
Test-Path artifacts/reports/phase1d_ablation_opponent_model/report.md
```

Expected:

- the full test suite passes;
- report artifacts exist;
- the task queue records L3 evidence paths for `task_6b` and `task_11a`
  through `task_11d`;
- all Phase 1D tasks are completed;
- the next work item is Phase 1E, not another Phase 1D task.

## Evaluation config change

Run:

```powershell
python -m pytest tests/integration/test_evaluation_config.py
scripts/dev/run_smoke_eval.ps1
```

## Research-only change

Run the experiment command listed in the relevant `research/.../README.md`.

Mainline smoke is required only if promotion to `src/sc2bot/` is requested.

## Phase A ladder infrastructure and baseline dataset

### A1 infrastructure gate

Evidence:

- `artifacts/reports/phase_a_ladder_infra_dataset/a1_infrastructure_gate/summary.json`
- `artifacts/reports/phase_a_ladder_infra_dataset/a1_infrastructure_gate/report.md`

Expected:

- one real probe and one 4-match real smoke are summarized;
- the report states this is infrastructure evidence only;
- the report does not claim bot strength.

### Baseline Dataset V0 manifest

Run:

```powershell
python -m evaluation.metrics.dataset_manifest `
  --source-manifest data/logs/evaluation/phase_a_baseline_v0/phase_a_baseline_v0_chunk_1/dataset_manifest.json `
  --source-manifest data/logs/evaluation/phase_a_baseline_v0/phase_a_baseline_v0_chunk_2/dataset_manifest.json `
  --source-manifest data/logs/evaluation/phase_a_baseline_v0/phase_a_baseline_v0_chunk_3/dataset_manifest.json `
  --output data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json `
  --run-id phase_a_baseline_v0 `
  --purpose "Phase A baseline real-match dataset V0 merged manifest" `
  --min-match-count 24
```

Expected:

- merged manifest exists at
  `data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json`;
- `match_count` is at least 24;
- included source manifests are explicit;
- historical exclusions are explicit;
- artifact completeness summarizes result, replay, and telemetry availability.

### Baseline Dataset V0 quality report

Run:

```powershell
python -m evaluation.reports.run_phase_a_dataset_quality_report `
  --manifest data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json `
  --output-dir artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality
```

Expected:

- `summary.json` and `report.md` are generated;
- report uses real baseline dataset outputs;
- report includes match count, maps, opponent races/difficulties, status
  distribution, crash/timeout rate, replay/telemetry availability, telemetry
  event coverage, duration summary, and known behavior limitations;
- report does not claim bot strength or gameplay quality.

### Scalable collection config

Run:

```powershell
python -m evaluation.runner.build_collection_config `
  --level smoke `
  --run-id phase_a_collection_smoke_dry_example `
  --output artifacts/reports/phase_a_ladder_infra_dataset/collection_config_examples/smoke_dry.yaml
```

Expected:

- generated config defaults to `launch_mode: dry_run`;
- generated config uses `isolate_runs: true`;
- generated config records `include_historical_by_default: false`;
- large real collection configs require explicit `--allow-large-real`.

## Phase 1E minimal strategy intervention

### Dry strategy response telemetry

Run:

```powershell
python -m pytest tests/unit/test_strategy_manager.py tests/unit/test_game_loop.py tests/unit/test_telemetry_schema.py
```

Expected:

- `StrategyResponse` serializes for telemetry;
- tag-only response selection works from synthetic predictions;
- dry telemetry records `strategy_response` and `strategy_switch`.

### Real strategy response probe

Run from Windows PowerShell:

```powershell
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
@'
from evaluation.runner.run_match import MatchRequest, run_match
print(run_match(MatchRequest(
    bot_config='configs/bot/opponent_model_tag_only.yaml',
    bot_config_id='tag_only',
    map_id='incorporeal_aie_v4',
    map_name='IncorporealAIE_v4',
    map_file='IncorporealAIE_v4.SC2Map',
    opponent_id='builtin_easy_terran',
    opponent_type='computer',
    opponent_race='terran',
    opponent_difficulty='easy',
    output_dir='data/logs/evaluation/phase1e_task5_tag_only_probe',
    launch_mode='real_launch',
)))
'@ | python -
```

Expected:

- real telemetry contains `opponent_prediction`, `strategy_response`, and
  `strategy_switch`;
- `strategy_response` includes `selected_response_tag` and
  `strategy_switch_reason`.

### Real small ablation and report

Run from Windows PowerShell:

```powershell
$repo = "\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai"
Set-Location $repo
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python evaluation/runner/run_batch.py --config configs/evaluation/phase1e_strategy_intervention_ablation.yaml
python -m evaluation.reports.run_strategy_intervention_report `
  --evaluation-dir data/logs/evaluation/phase1e_strategy_intervention_ablation/20260421T145911Z `
  --output-dir artifacts/reports/phase1e_strategy_intervention `
  --run-id 20260421T145911Z
```

Expected:

- 1 map x 2 opponents x 3 configs produce 6 real match directories;
- every match has `match_result.json`, `match.SC2Replay`, and
  `telemetry/events.jsonl`;
- report artifacts exist;
- report states it does not prove win-rate or gameplay-quality improvement.

## Phase B playable competitive core

### Focused unit/dry checks

Run:

```powershell
python -m pytest tests/unit/test_tactical_manager.py tests/unit/test_game_loop.py tests/unit/test_telemetry_schema.py
```

Expected:

- tactical plan serialization works;
- minimal `army_rally`, `defend_order`, and `attack_order` selection is covered
  by synthetic tests;
- combat event telemetry serializes and records structured no-combat reasons.

### Small real evaluation

Run from Windows PowerShell:

```powershell
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python -m evaluation.runner.run_batch --config configs/evaluation/phase_b_small_eval.yaml
```

Expected:

- 1 map x 4 built-in opponents x 2 repeats produces 8 real match directories;
- every match has `match_result.json`, `match.SC2Replay`, and
  `telemetry/events.jsonl`;
- `summary.json` exists under the run directory;
- crash/timeout/missing artifact counts can be computed;
- current known limitation: this run does not prove friendly army production or
  bot strength.

### Phase B report

Run:

```powershell
python -m json.tool artifacts/reports/phase_b_playable_competitive_core/summary.json
Test-Path artifacts/reports/phase_b_playable_competitive_core/report.md
```

Expected:

- `summary.json` is valid JSON;
- report uses real task 13 data;
- report states whether Level 1 playable baseline is reached;
- current report states Level 1 is not reached;
- report does not claim ladder competitiveness, gameplay quality, or
  opponent-model outcome improvement.
