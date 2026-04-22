# Master Plan: Interview Demo V0

Status: paused / superseded as the active route on 2026-04-21.

Superseded by: `docs/plans/active/ladder_ready_adaptive_sc2_bot_roadmap.md`

Reason: Phase 1D and Phase 1E validated runtime, telemetry, opponent prediction, strategy response, reporting, and L3 validation mechanics, but they do not prove ladder readiness or playable competitive quality. Phase 1F demo packaging is paused until the bot has a ladder-ready playable core.

## Summary

Build a real, reproducible, interview-ready StarCraft II AI demo that can run
local full-game matches, record live `GameState` and `ScoutingObservation`
telemetry, execute rule-based opponent-model predictions, run null vs
rule_based ablations, and generate readable experiment reports.

This plan optimizes for a clear engineering/research loop, not ladder strength:

- real full-game execution;
- opponent-modeling experiment closure;
- explainable telemetry;
- reproducible reports;
- stable interview demonstration.

## Execution Rules

- This master plan defines route and acceptance gates only.
- Do not implement all milestones at once.
- The only milestone currently allowed for execution is Milestone 1:
  Phase 1D Opponent Modeling Ablation V0.
- Keep mainline code in `src/sc2bot/`; do not import `research/` into mainline.
- Keep evaluation orchestration in `evaluation/`; do not place bot decisions there.
- Do not add SMAC, LLM real-time control, world-model-lite, replay imitation, or
  complex strategy unless a later milestone explicitly approves it.
- After each milestone, update:
  - `docs/context/current_status.md`
  - `docs/context/validated_findings.md`
  - `docs/context/open_hypotheses.md`
  - `docs/handoffs/latest.md`
  - `docs/commands/verification_matrix.md`
- If a milestone fails, stop and write a failure note before changing scope.

## Milestone 0: Completed Runtime + Observation Foundation

### Goal

Record the already-completed foundation that makes the demo path possible.

### Scope

- Bare `python-sc2` / BurnySC2 engineering base selected.
- WSL development environment can drive Windows StarCraft II.
- Real local match on installed maps works.
- Telemetry, replay, replay metadata, and match result persistence work.
- Survival baseline runs to a configured runtime limit.
- Live `GameState` and `ScoutingObservation` telemetry exists.
- Worker scout produces non-empty opponent observations.
- Small built-in opponent pool can run in batch.
- `opponent_model.mode: null | rule_based` config switch exists.

### Non-goals

- No new implementation.
- No new strategy behavior.
- No expansion of opponent pool or maps in this milestone.

### Files Likely To Change

- None. This milestone is already complete.

### Verification

- Existing recorded evidence in `docs/context/validated_findings.md`.
- Existing real outputs under `data/logs/evaluation/phase1c_*`.
- `python -m pytest tests`.

### Done Criteria

- Foundation capabilities are documented and available for Milestone 1.

### Stop Conditions

- If any foundation capability is found to be broken, stop and restore that
  capability before continuing to Milestone 1.

## Milestone 1: Phase 1D Opponent Modeling Ablation V0

### Goal

Create the first opponent-modeling experiment loop with prediction-only
rule-based modeling and null vs rule_based ablation.

### Scope

- Minimal Protoss supply sustain.
- Rule-based opponent model v0.
- `opponent_prediction` telemetry for both null and rule_based modes.
- Telemetry feature extractor v0.
- Null vs rule_based ablation config.
- Machine-readable `summary.json`.
- Short markdown `report.md`.

### Non-goals

- Do not claim win-rate improvement.
- Do not let rule_based predictions change gameplay behavior.
- Do not add complex build order, gas, army production, expansion, SMAC, LLM, or
  replay learning.

### Files Likely To Change

- `src/sc2bot/runtime/game_loop.py`
- `src/sc2bot/opponent_model/interface.py`
- `src/sc2bot/opponent_model/null_model.py`
- `src/sc2bot/opponent_model/rule_based_model.py`
- `src/sc2bot/config/schema.py`
- `src/sc2bot/config/loader.py`
- `evaluation/runner/run_batch.py`
- `evaluation/metrics/feature_extractor.py`
- `evaluation/metrics/opponent_model_metrics.py`
- `evaluation/reports/`
- `configs/bot/`
- `configs/evaluation/`
- `tests/`
- milestone status docs listed in Execution Rules.

### Verification

- `python -m pytest tests`
- One real match with `opponent_model.mode = null`.
- One real match with `opponent_model.mode = rule_based`.
- Real ablation batch with at least 2 opponents x 2 bot configs.
- Feature extraction from real telemetry.
- Generated:
  - `artifacts/reports/phase1d_ablation_opponent_model/summary.json`
  - `artifacts/reports/phase1d_ablation_opponent_model/report.md`

### Done Criteria

- Supply sustain telemetry shows pylon attempt/success/skip/failure reasons.
- Null and rule_based both emit `opponent_prediction` telemetry.
- Rule-based predictions produce interpretable risk signals from live scouting.
- Feature extractor handles missing fields without crashing.
- Ablation report states prediction-only limitations and does not claim
  performance improvement.

### Stop Conditions

- Real matches fail to launch through the project runner.
- Supply sustain causes runtime crashes.
- Feature extraction cannot process real telemetry.
- Report wording implies unsupported win-rate or gameplay improvement.

## Milestone 2: Phase 1E Minimal Strategy Intervention V0

### Goal

Allow opponent-model predictions to lightly influence strategy response tags,
while keeping behavior minimal and explainable.

### Scope

- Feed opponent prediction into `StrategyManager` as a first-class decision
  input.
- Add config-gated strategy intervention mode.
- Map high `rush_risk` / `tech_risk` to response tags.
- Record `strategy_switch_reason` and consumed prediction fields in telemetry.
- Keep the intervention small enough to compare against prediction-only Phase 1D.

### Non-goals

- No full build order.
- No army production system.
- No expansion system.
- No learning or policy model.
- No claim of improved strength unless verified by ablation.

### Files Likely To Change

- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/domain/decisions.py`
- `src/sc2bot/runtime/game_loop.py`
- `configs/bot/`
- `configs/evaluation/`
- `evaluation/metrics/opponent_model_metrics.py`
- `tests/`
- milestone status docs listed in Execution Rules.

### Verification

- `python -m pytest tests`
- Real match with intervention disabled matches Phase 1D behavior.
- Real match with intervention enabled records `strategy_switch_reason`.
- Ablation report compares prediction-only vs intervention-enabled configs.

### Done Criteria

- Strategy tags change only when configured.
- Telemetry explains why any response tag changed.
- The ablation report separates prediction quality from behavior intervention.

### Stop Conditions

- Intervention changes gameplay when disabled.
- Strategy logic expands into a broad build-order system.
- Telemetry cannot explain a strategy switch.
- Results are too noisy to interpret and no failure note is written.

## Milestone 3: Phase 1F Demo Report V0

### Goal

Generate an interview-readable report from telemetry and ablation outputs.

### Scope

- Produce a readable report with:
  - prediction timeline;
  - scouting timeline;
  - ablation summary;
  - key telemetry examples;
  - known limitations;
  - next experiment recommendation.
- Keep machine-readable JSON alongside markdown.
- Prefer deterministic local generation from saved match outputs.

### Non-goals

- No LLM replay summary.
- No subjective replay narration.
- No manual report editing as the primary path.
- No new gameplay behavior.

### Files Likely To Change

- `evaluation/reports/`
- `evaluation/metrics/`
- `artifacts/reports/`
- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`
- milestone status docs listed in Execution Rules.

### Verification

- `python -m pytest tests`
- Generate report from Phase 1D or Phase 1E outputs.
- Confirm report includes prediction timeline, scouting timeline, ablation
  summary, and known limitations.
- Confirm report can be regenerated from commands without notebook state.

### Done Criteria

- Report is readable without inspecting raw JSONL.
- Report links or names the replay, match result, and telemetry sources.
- Report does not overstate bot strength or opponent-model impact.

### Stop Conditions

- Report requires notebook-only state.
- Report generation depends on chat history.
- Report content becomes a showcase layer that obscures experiment limitations.

## Milestone 4: Phase 1G Demo Freeze

### Goal

Freeze a reproducible interview demo version with stable commands, configs,
replays, and reports.

### Scope

- Fix the demo map list.
- Fix the opponent pool.
- Fix the bot configs used for demo.
- Save or reference canonical replay and report artifacts.
- Add README demo instructions.
- Record exact verification commands and expected outputs.

### Non-goals

- No new research feature.
- No new strategy expansion.
- No broad refactor.
- No pursuit of ladder strength.

### Files Likely To Change

- `README.md`
- `docs/commands/common_commands.md`
- `docs/commands/verification_matrix.md`
- `configs/evaluation/`
- `configs/opponents/`
- `artifacts/reports/`
- milestone status docs listed in Execution Rules.

### Verification

- Fresh run of the frozen demo commands.
- Confirm replay, telemetry, match result, summary, and report paths exist.
- Confirm README instructions are sufficient to reproduce the demo on the
  configured local machine.

### Done Criteria

- A reviewer can run the documented command sequence and reproduce the demo.
- Frozen outputs clearly show:
  - real SC2 match execution;
  - live observation telemetry;
  - opponent prediction;
  - ablation comparison;
  - known limitations.

### Stop Conditions

- Demo requires undocumented local state.
- Frozen commands are flaky across repeated local runs.
- README implies the bot is stronger or more complete than the evidence shows.
