# Repository Skeleton Manifest

Initial skeleton created for the SC2 AI project.

## Root

- `README.md`
- `AGENTS.md`
- `pyproject.toml`
- `.gitignore`
- `requirements/base.txt`
- `requirements/dev.txt`
- `requirements/bot.txt`
- `requirements/research.txt`

## Mainline

- `src/sc2bot/main.py`
- `src/sc2bot/runtime/bot_app.py`
- `src/sc2bot/runtime/game_loop.py`
- `src/sc2bot/runtime/dependency_container.py`
- `src/sc2bot/managers/macro_manager.py`
- `src/sc2bot/managers/scouting_manager.py`
- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/managers/tactical_manager.py`
- `src/sc2bot/managers/micro_manager.py`
- `src/sc2bot/opponent_model/interface.py`
- `src/sc2bot/opponent_model/null_model.py`
- `src/sc2bot/opponent_model/rule_based_model.py`
- `src/sc2bot/telemetry/event_logger.py`
- `src/sc2bot/telemetry/schema.py`
- `src/sc2bot/telemetry/replay_index.py`
- `src/sc2bot/config/loader.py`
- `src/sc2bot/config/schema.py`
- `src/sc2bot/domain/game_state.py`
- `src/sc2bot/domain/observations.py`
- `src/sc2bot/domain/decisions.py`
- `src/sc2bot/domain/constants.py`

## Governance

- `docs/context/`
- `docs/adr/`
- `docs/plans/`
- `docs/handoffs/`
- `docs/lessons/`
- `docs/templates/`
- `docs/commands/`

## Research

- `research/opponent_modeling/`
- `research/replay_learning/`
- `research/smac_micro/`
- `research/llm_coach/`
- `research/combat_predictor/`
- `research/ablations/`

## Evaluation

- `evaluation/runner/`
- `evaluation/metrics/`
- `evaluation/opponent_pool/`

## Tests and Scripts

- `tests/unit/`
- `tests/integration/`
- `scripts/setup/`
- `scripts/dev/`
- `scripts/data/`
- `scripts/docs/`
