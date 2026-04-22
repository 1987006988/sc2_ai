# Phase 1E Minimal Strategy Intervention V0

- Run timestamp: `2026-04-21T15:19:29.071951+00:00`
- Run id: `20260421T145911Z`
- Evaluation dir: `data/logs/evaluation/phase1e_strategy_intervention_ablation/20260421T145911Z`
- Output scope: `evaluation_dir`
- Match count: `6`
- Maps: incorporeal_aie_v4
- Opponents: builtin_easy_terran, builtin_easy_zerg
- Bot configs: minimal_behavior, null, rule_based_prediction_only

## Status Counts

- `max_game_time_reached`: 6

## Bot Config Comparison

### minimal_behavior

- Matches: `2`
- Status counts: `{'max_game_time_reached': 2}`
- Opponent model modes: `rule_based`
- Intervention modes: `minimal_behavior`
- Prediction rush risk max: `0.55`
- Prediction tech risk max: `0.5`
- Prediction confidence max: `0.65`
- Selected response tag count: `773`
- Strategy switch count: `8`
- Defensive posture count: `100`
- Continue scouting count: `456`
- Tech alert count: `217`
- Minimal behavior intervention count: `1758`
- Minimal behavior active count: `456`
- Minimal behavior skipped count: `1302`

### null

- Matches: `2`
- Status counts: `{'max_game_time_reached': 2}`
- Opponent model modes: `null`
- Intervention modes: `none`
- Prediction rush risk max: `0.0`
- Prediction tech risk max: `0.0`
- Prediction confidence max: `0.0`
- Selected response tag count: `0`
- Strategy switch count: `2`
- Defensive posture count: `0`
- Continue scouting count: `0`
- Tech alert count: `0`
- Minimal behavior intervention count: `0`
- Minimal behavior active count: `0`
- Minimal behavior skipped count: `0`

### rule_based_prediction_only

- Matches: `2`
- Status counts: `{'max_game_time_reached': 2}`
- Opponent model modes: `rule_based`
- Intervention modes: `none`
- Prediction rush risk max: `0.55`
- Prediction tech risk max: `0.5`
- Prediction confidence max: `0.65`
- Selected response tag count: `0`
- Strategy switch count: `2`
- Defensive posture count: `0`
- Continue scouting count: `0`
- Tech alert count: `0`
- Minimal behavior intervention count: `0`
- Minimal behavior active count: `0`
- Minimal behavior skipped count: `0`

## Prediction Timeline Summary

- `reallaunch-ad89d057` / `minimal_behavior` / `builtin_easy_terran`: first_enemy_seen=40.53571428571429, rush_max=0.55, tech_max=0.5, selected_tags=425, switches=4, interventions=879
- `reallaunch-1c3ccc7d` / `minimal_behavior` / `builtin_easy_zerg`: first_enemy_seen=40.17857142857143, rush_max=0.55, tech_max=0.5, selected_tags=348, switches=4, interventions=879
- `reallaunch-d38f69a3` / `null` / `builtin_easy_terran`: first_enemy_seen=40.714285714285715, rush_max=0.0, tech_max=0.0, selected_tags=0, switches=1, interventions=0
- `reallaunch-a904a421` / `null` / `builtin_easy_zerg`: first_enemy_seen=39.642857142857146, rush_max=0.0, tech_max=0.0, selected_tags=0, switches=1, interventions=0
- `reallaunch-b5b1667b` / `rule_based_prediction_only` / `builtin_easy_terran`: first_enemy_seen=40.714285714285715, rush_max=0.55, tech_max=0.5, selected_tags=0, switches=1, interventions=0
- `reallaunch-5b92e21b` / `rule_based_prediction_only` / `builtin_easy_zerg`: first_enemy_seen=39.285714285714285, rush_max=0.55, tech_max=0.5, selected_tags=0, switches=1, interventions=0

## Interpretation

This is a minimal strategy-intervention telemetry ablation. It validates that predictions can be converted into response tags and that the `minimal_behavior` path can emit observable intervention telemetry. It does not prove win-rate improvement or gameplay quality improvement.

Prediction metrics summarize `opponent_prediction` events. Response-tag metrics summarize `strategy_response` and `strategy_switch` events. Intervention metrics summarize `minimal_behavior_intervention` events.

## Known Limitations

- This is a minimal intervention telemetry ablation.
- The intervention is intentionally thin and config-gated.
- This report does not prove win-rate improvement.
- This report does not prove gameplay quality improvement.
- Response tags and intervention counts show that code paths executed, not that decisions are strategically optimal.

## Next Experiment

Review response-tag and intervention telemetry before deciding whether any minimal behavior should be retained for a demo freeze.
