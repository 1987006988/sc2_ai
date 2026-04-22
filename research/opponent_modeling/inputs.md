# Opponent Model Prototype Inputs

This prototype must remain compatible with the production interface in `src/sc2bot/opponent_model/`, but the research layer may enrich features as needed.

## Minimum Phase-1 Inputs

- `game_loop`
- `enemy_units_seen`
- `enemy_structures_seen`
- `enemy_expansions_seen`

## Suggested Derived Inputs

- first observed tech structure timing
- first observed combat unit timing
- number of distinct enemy production structures seen
- time since last scout
- own current strategy tag

## Data Sources

Phase 1 should prefer:

- telemetry logs from mainline dry-run or local matches;
- replay metadata;
- small extracted replay features if available.

Do not make the prototype depend on a large replay-processing pipeline in order to start.
