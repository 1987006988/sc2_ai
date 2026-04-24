# sc2-ai

Layered hybrid full-game StarCraft II bot project using bare `python-sc2`
(`burnysc2`) as the current engineering base.

## Goal

The long-term goal is a single-race Protoss bot that can run repeated
ladder-like bot-vs-bot matches, collect real match evidence, and use opponent
modeling / hidden-state inference as a research feature.

The current mainline objective is narrower and stricter:

1. first reach an accepted playable baseline;
2. then validate a single adaptive research feature on top of that baseline.

This project is not trying to be an AlphaStar clone, a pure SMAC project, or an
LLM real-time controller.

## Current Control Layer

The active control layer is now established. The current execution authority is:

- `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/experiments/real_match_validation_protocol.md`
- `docs/experiments/checkpoint_acceptance_spec.md`
- `docs/plans/active/phase_playable_core_rebuild.md`
- `docs/plans/active/phase_adaptive_response_research.md`
- `docs/agents/codex_execution_rules_research_mode.md`
- `docs/templates/task_recipe_template.md`
- `docs/experiments/failure_repair_playbook.md`

The current mainline sequence is:

1. playable core rebuild
2. adaptive response research

Old Phase A / Phase B / Phase B-R plans, queues, and manual triggers are
retained only as historical or diagnostic reference. They no longer directly
drive execution.

## Current Status

What is true right now:

- real SC2 local-match launching, artifact persistence, dataset manifests, and
  reporting infrastructure have been validated;
- the new research control layer has been imported and cleaned up;
- old plans have been downgraded to historical reference;
- the repository can now begin from the new master queue;
- this cleanup round did not add any new gameplay capability.

What is not true yet:

- there is no accepted playable Protoss combat core yet;
- there is no validated Level 1 baseline yet;
- there is no validated adaptive research contribution yet;
- the repository does not prove ladder competitiveness.

## Real-Match-First Rules

- Unit tests prove code logic only.
- Dry-runs prove orchestration only.
- Real matches are required to prove gameplay behavior.
- Multi-match batches are required to discuss stability.
- Reports must distinguish synthetic, dry-run, and real-match evidence.
- `completed` does not mean `validated`.
- `diagnostic` does not mean `capability`.
- Checkpoint failure blocks progression.

## Repository Layout

- `src/sc2bot/`: production bot runtime, managers, config, telemetry, and
  stable interfaces.
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

Generated logs, replays, checkpoints, and raw/intermediate data are
intentionally ignored by git.

## Historical References

Legacy planning materials are indexed in:

- `docs/plans/legacy_index.md`

They are still useful for historical reasoning and diagnostic provenance, but
they are no longer execution authority.

## What This Repository Does Not Prove Yet

- It does not prove ladder competitiveness.
- It does not prove stable win rate against built-in Easy or Medium opponents.
- It does not prove gameplay quality improvement.
- It does not prove opponent modeling improves match outcomes.
- It does not yet prove an accepted playable Protoss combat core.

## Next Step

If execution resumes, it should start from:

- `docs/plans/active/research_master_task_queue.yaml`

Do not resume from old Phase A / Phase B / Phase B-R queues.
