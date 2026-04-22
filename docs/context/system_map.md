# System Map

## Runtime Flow

```text
main.py
  -> runtime.BotApp
      -> Config
      -> Telemetry
      -> MacroManager
      -> ScoutingManager
      -> OpponentModel
      -> StrategyManager
      -> TacticalManager
      -> MicroManager
```

## Mainline Boundaries

- `src/sc2bot/`: production bot and stable interfaces.
- `research/`: prototypes only.
- `evaluation/`: batch runs and metrics.
- `data/`: logs, replays, datasets.
- `artifacts/`: generated reports and models.

## Current State

The system is currently a skeleton. Managers expose interfaces but do not implement advanced strategy.
