# Phase A Baseline Dataset V0 Quality Report

- Run id: `phase_a_baseline_v0`
- Evidence type: `real_match_baseline_dataset`
- Data source: `data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json`
- Match count: `24`
- Maps: `['incorporeal_aie_v4', 'leylines_aie_v3']`
- Opponent races: `{'protoss': 8, 'terran': 8, 'zerg': 8}`
- Opponent difficulties: `{'easy': 12, 'medium': 12}`
- Status counts: `{'max_game_time_reached': 24}`
- Crash rate: `0.0`
- Timeout rate: `0.0`
- Replay availability: `1.0`
- Telemetry availability: `1.0`

## Artifact Completeness

- Match results: `24`
- Replays: `24`
- Telemetry files: `24`
- Missing replays: `0`
- Missing telemetry: `0`

## Match Duration

- Duration seconds: `{'min': 26.464161, 'max': 29.871431, 'avg': 28.201297583333332}`

## Telemetry Event Coverage

- `match_started`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 24}`
- `sc2_match_started`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 24}`
- `game_state`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 15624}`
- `scouting_observation`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 15624}`
- `opponent_prediction`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 15624}`
- `strategy_response`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 15624}`
- `sc2_match_exit_requested`: `{'matches_with_event': 24, 'match_coverage_rate': 1.0, 'event_count': 24}`

## Scout Timing

- First enemy seen time seconds: `{'min': 39.10714285714286, 'max': 41.964285714285715, 'avg': 40.50548748824611}`
- First scout dispatch time seconds: `{'min': None, 'max': None, 'avg': None, 'reason': 'worker_scout_dispatched telemetry currently has no game_time field'}`
- Scout dispatch event count: `24`

## Current Bot Behavior Limitations

- Baseline dataset is collected from the current survival/opponent-model scaffold, not a playable competitive core.
- All 24 matches ended with max_game_time_reached, so this dataset does not measure wins or losses as a strength claim.
- Current telemetry has scout dispatch events but no game_time on those events, so first_scout_time is unknown.
- Combat and build progression quality are not established by this report.
- This report does not prove bot strength, ladder competitiveness, or gameplay improvement.

## Interpretation

- This report uses real Phase A baseline match outputs.
- It measures dataset and artifact quality, not bot strength.
- It does not prove ladder competitiveness, win-rate quality, or gameplay improvement.
- Synthetic and dry-run evidence are not used for capability claims in this report.
