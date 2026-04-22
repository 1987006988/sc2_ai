# Opponent Model Prototype Outputs

Outputs must stay semantically compatible with the production `OpponentPrediction` interface.

## Minimum Phase-1 Outputs

- `opening_type`
- `rush_risk`
- `tech_risk`
- `enemy_army_estimate`
- `confidence`
- `recommended_response_tags`

## Output Semantics

- `opening_type`: coarse opponent opening label, e.g. `unknown`, `rush`, `greedy_expand`, `teching`
- `rush_risk`: normalized scalar in `[0, 1]`
- `tech_risk`: normalized scalar in `[0, 1]`
- `enemy_army_estimate`: coarse categorical estimate
- `confidence`: confidence in the current prediction
- `recommended_response_tags`: high-level action hints such as `scout_more`, `hold_ramp`, `delay_expand`
