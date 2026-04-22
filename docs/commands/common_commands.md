# Common Commands

From repository root:

```powershell
$env:SC2PATH = "D:\games\StarCraft II"
scripts/setup/check_env.ps1
scripts/dev/run_bot_local.ps1
scripts/dev/run_smoke_eval.ps1
python -m pytest tests/unit
```

`SC2PATH` is the canonical environment variable for the StarCraft II installation root.

Current local example:

`D:\games\StarCraft II`

Current installed test maps:

- `IncorporealAIE_v4.SC2Map`
- `LeyLinesAIE_v3.SC2Map`

Use `scripts/setup/check_env.ps1` to verify:

- `SC2PATH` exists;
- the SC2 root layout is valid;
- the project can resolve the installation before attempting real launch.

Minimal real-launch probe:

```powershell
$env:SC2PATH = "D:\games\StarCraft II"
$env:PYTHONPATH = "src;."
@'
from evaluation.runner.run_match import MatchRequest, run_match
print(run_match(MatchRequest(
    bot_config='configs/bot/debug.yaml',
    map_id='incorporeal_aie_v4',
    map_name='IncorporealAIE_v4',
    map_file='IncorporealAIE_v4.SC2Map',
    opponent_id='builtin_easy_terran',
    opponent_type='computer',
    opponent_race='terran',
    opponent_difficulty='easy',
    output_dir='data/logs/evaluation/real_launch_probe',
    launch_mode='real_launch',
)))
'@ | python -
```

Phase 1C real smoke batch from WSL through Windows PowerShell:

```powershell
$repo = "\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai"
Set-Location $repo
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python evaluation/runner/run_batch.py --config configs/evaluation/phase1c_real_smoke.yaml
```

Expected outputs:

- per-match `match_result.json`;
- per-match `telemetry/events.jsonl`;
- per-match `match.SC2Replay`;
- `data/logs/evaluation/phase1c_real_smoke/summary.json`.

Phase 1D opponent-model ablation:

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

Expected report outputs:

- `artifacts/reports/phase1d_ablation_opponent_model/summary.json`
- `artifacts/reports/phase1d_ablation_opponent_model/report.md`

Validated Phase 1D L3 evidence examples:

- rule-based telemetry probe:
  `data/logs/evaluation/phase1d_task6b_probe/reallaunch-f4b16b51/`
- null single match:
  `data/logs/evaluation/phase1d_task11a_null_match/reallaunch-b111cf67/`
- rule-based single match:
  `data/logs/evaluation/phase1d_task11b_rule_based_match/reallaunch-edba8ac0/`
- real ablation batch summary:
  `data/logs/evaluation/phase1d_ablation_opponent_model/summary.json`

Note: repeated real batches can append historical match directories under the
same output root. Use fresh output directories or recorded run ids when a clean
match count is required.

Phase 1E minimal strategy intervention ablation:

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

Validated Phase 1E L3 evidence examples:

- tag-only telemetry probe:
  `data/logs/evaluation/phase1e_task5_tag_only_probe/reallaunch-350f1ad9/`
- minimal_behavior telemetry probe:
  `data/logs/evaluation/phase1e_task7_minimal_behavior_probe/reallaunch-0997c3b4/`
- real small ablation:
  `data/logs/evaluation/phase1e_strategy_intervention_ablation/20260421T145911Z/`
- report outputs:
  `artifacts/reports/phase1e_strategy_intervention/summary.json`
  and `artifacts/reports/phase1e_strategy_intervention/report.md`

Phase A package dry-run check:

```powershell
$env:PYTHONPATH = "src;."
python -m evaluation.runner.package_dry_run --output artifacts/package_dry_run/manifest.json
```

This is dry evidence only. It checks entrypoint/config/script/package-manifest
readiness and does not upload, launch SC2, or prove bot strength.

Phase A reusable collection config generation:

```powershell
$env:PYTHONPATH = "src;."
python -m evaluation.runner.build_collection_config `
  --level smoke `
  --run-id phase_a_collection_smoke_YYYYMMDD `
  --output artifacts/reports/phase_a_ladder_infra_dataset/collection_config_examples/smoke_dry.yaml
```

Collection levels:

- `smoke`: 4 expected matches.
- `baseline`: 24 expected matches.
- `evaluation`: 60 expected matches.
- `regression`: 12 expected matches by default; override with `--repeats`.

The generated config defaults to `launch_mode: dry_run`; this is orchestration
evidence only and does not prove bot strength. To intentionally create a real
collection config, pass `--launch-mode real_launch`. Large real collections
at or above 50 expected matches require `--allow-large-real`.

Run a generated dry config:

```powershell
$env:PYTHONPATH = "src;."
python -m evaluation.runner.run_batch --config artifacts/reports/phase_a_ladder_infra_dataset/collection_config_examples/smoke_dry.yaml
```

Historical runs are not mixed by default: generated configs set
`isolate_runs: true`, require a caller-provided `run_id`, and record
`include_historical_by_default: false`.

Phase A closeout evidence:

```powershell
Test-Path data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json
Test-Path artifacts/reports/phase_a_ladder_infra_dataset/a1_infrastructure_gate/summary.json
Test-Path artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/summary.json
Test-Path artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/report.md
```

Baseline V0 summary:

- 24 real match attempts;
- 2 maps: `incorporeal_aie_v4`, `leylines_aie_v3`;
- built-in Terran/Zerg/Protoss opponents at Easy/Medium;
- all matches have result, replay, and telemetry artifacts;
- this is infrastructure and dataset evidence only, not a bot-strength claim.

Phase B small real evaluation:

```powershell
$env:PYTHONPATH = "src;."
$env:SC2PATH = "D:\games\StarCraft II"
python -m evaluation.runner.run_batch --config configs/evaluation/phase_b_small_eval.yaml
```

Expected outputs:

- run directory:
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`;
- per-match `match_result.json`, `match.SC2Replay`, and
  `telemetry/events.jsonl`;
- batch `summary.json`;
- task metrics:
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/phase_b_small_eval_metrics.json`.

Phase B report artifacts:

```powershell
Test-Path artifacts/reports/phase_b_playable_competitive_core/summary.json
Test-Path artifacts/reports/phase_b_playable_competitive_core/report.md
```

Current Phase B conclusion:

- 8 real matches ran with complete result/replay/telemetry artifacts;
- Gateway build commands succeeded in all 8 matches;
- combat-unit production success count is 0;
- no telemetry event reported `own_army_count > 0`;
- all 8 matches ended as `Result.Defeat`;
- this does not prove Level 1 playable baseline, gameplay quality, or ladder
  competitiveness.
