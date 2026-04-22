# sc2-ai

Layered hybrid full-game StarCraft II bot project using bare `python-sc2`
(`burnysc2`) as the current engineering base.

## Goal

The long-term goal is a single-race Protoss bot that can run repeated
ladder-like bot-vs-bot matches, collect real match evidence, and use opponent
modeling / hidden-state inference as its main research feature.

This project is not trying to be an AlphaStar clone, a pure SMAC project, or an
LLM real-time controller.

## Current Status

Phase A, Ladder Infrastructure & Scalable Real-Match Dataset, has been accepted.
The project can launch real local SC2 matches, persist match artifacts, generate
dataset manifests, and produce infrastructure/data-quality reports.

Phase B, Playable Competitive Core, is not accepted yet. The Phase B evidence
audit found that several tasks were completed diagnostically, but the real
matches ended at about `116.07` game seconds because of the current runtime
limit. That is too short to validate Cyber Core, combat-unit production,
attack/defend behavior, or friendly combat.

Current validated capability is infrastructure and telemetry, not bot strength.

## Real-Match-First Rules

- Unit tests prove code logic only.
- Dry-runs prove orchestration only.
- Real matches are required to prove gameplay behavior.
- Multi-match batches are required to discuss stability.
- Reports must distinguish synthetic, dry-run, and real-match evidence.
- Do not claim win-rate, gameplay quality, or ladder competitiveness unless the
  collected real-match data supports it.

## Repository Layout

- `src/sc2bot/`: production bot runtime, managers, config, telemetry, and stable
  interfaces.
- `evaluation/`: match runners, batch orchestration, metrics, and reports.
- `configs/`: bot, map, opponent, evaluation, and collection configs.
- `research/`: isolated prototypes and research notes; not imported by
  `src/sc2bot/`.
- `docs/`: project memory, plans, handoffs, findings, and command references.
- `tests/`: unit and integration tests.

Read `AGENTS.md` before making changes.

## Requirements

- Windows StarCraft II installation.
- `SC2PATH` pointing at the StarCraft II root, for example:

```powershell
$env:SC2PATH = "D:\games\StarCraft II"
```

- Python environment with project dependencies installed, including
  `burnysc2==7.2.1`.
- Local maps installed under the SC2 `Maps` directory.

## Run Tests

From the repository root:

```bash
python -m pytest tests
```

Focused unit tests can be run with:

```bash
python -m pytest tests/unit
```

## Run A Real Local Match

Real SC2 matches are launched from WSL through Windows PowerShell/Python on this
machine. A typical pattern is:

```bash
powershell.exe -NoProfile -Command "$repo='\\wsl.localhost\segment-anything-2\home\taotao\sc2-ai'; Set-Location $repo; $env:PYTHONPATH='src;.'; $env:SC2PATH='D:\games\StarCraft II'; python evaluation/runner/run_match.py --config configs/evaluation/smoke.yaml --launch-mode real_launch"
```

Exact commands and validated variants are tracked in:

- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`
- `docs/handoffs/latest.md`

Generated logs, replays, checkpoints, and raw/intermediate data are intentionally
ignored by git.

## Current Reports

- Phase A dataset quality:
  `artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/`
- Phase B evidence audit:
  `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`
- Phase B report:
  `artifacts/reports/phase_b_playable_competitive_core/report.md`

## What This Repository Does Not Prove Yet

- It does not prove ladder competitiveness.
- It does not prove stable win rate against built-in Easy or Medium opponents.
- It does not prove gameplay quality improvement.
- It does not prove opponent modeling improves match outcomes.
- It does not yet prove a playable Protoss combat core.

The next engineering priority is a focused Phase B follow-up: fix or
parameterize the real-match duration window, then rerun Gateway-ready,
Cyber Core, combat-unit production, attack/defend, and friendly-combat probes.
