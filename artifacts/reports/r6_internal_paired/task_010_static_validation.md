# R6 Task 010 Static Validation

Date: 2026-04-26

## Scope

- integrated learned temporal belief runtime wrapper
- added config-separated learned treatment
- added bounded production tempo gate
- preserved frozen baseline and frozen R5 comparator configs

## Verification

```bash
PYTHONPATH=.:src python -m pytest \
  tests/unit/test_strategy_manager.py \
  tests/unit/test_game_loop.py \
  tests/r6/test_temporal_model_interface.py \
  tests/r6/test_online_belief_gating.py \
  tests/unit/test_config_loader.py -q
```

Result:

```text
62 passed in 0.90s
```

Runtime smoke:

```bash
PYTHONPATH=.:src python -c "from pathlib import Path; from sc2bot.runtime.bot_app import BotApp; app=BotApp.from_config(Path('configs/bot/r6_learned_belief.yaml')); app.initialize(); app.run(); print(app.container.opponent_model_mode)"
```

Result:

```text
learned_temporal_belief
```

## Outcome

- learned temporal belief treatment is config-separated and auditable
- bounded production tempo is wired into runtime behavior
- learned runtime now uses current-visibility combat cues rather than sticky
  ever-seen combat sets
- learned production tempo requires fresher scout evidence and no longer latches
  on stale tech sightings
- fallback deployment artifact exists for online environments without `torch`
- frozen baseline and frozen comparator remained unchanged
