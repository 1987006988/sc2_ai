# Phase B Evidence Audit And Capability Reclassification

Date: 2026-04-22

## Purpose

This audit separates:

- task execution completed;
- diagnostic completed;
- gameplay capability validated.

The previous Phase B queue marked tasks as `completed` when they produced the
requested artifact or telemetry evidence. That was useful task execution
tracking, but it overstates gameplay capability for tasks whose real matches
ended before the minimum opportunity window for the target behavior.

## Cutoff Diagnosis

Observed real-match cutoff:

- all audited probes and all 8 small-eval matches ended around
  `game_time=116.07`;
- `match_result.json` status: `max_game_time_reached`;
- failure reason: `null`;
- replay and telemetry artifacts were present.

Cutoff source:

- primary cutoff: bot self-exit in `src/sc2bot/runtime/game_loop.py`;
- controlling config: `configs/bot/debug.yaml`;
- value: `runtime.max_game_loop: 2600`;
- conversion: `2600 / 22.4 = 116.07` game seconds;
- runner also sets `game_time_limit=120` in `evaluation/runner/run_match.py`,
  but the evidence shows the bot reached its own `max_game_time_reached` exit.

This was not a launch failure, SC2 process issue, timeout, or artifact failure.

## Required Minimum Opportunity Windows

These windows are conservative acceptance thresholds for validating capability,
not exact StarCraft II balance timings.

- Gateway command telemetry: 90 seconds.
- Gateway completion / ready gateway: 140 seconds.
- Assimilator + Cyber Core opportunity: 180 seconds.
- First Zealot/Stalker production opportunity: 200 seconds.
- Friendly army order opportunity: 220 seconds.
- Friendly combat opportunity: 240 seconds.
- Small eval playable-baseline opportunity: at least 240 seconds per match.

The current 116.07-second window is below every post-Gateway capability window.

## Reclassification Summary

| Task | Original status | Original level | Real SC2 | Actual game time | Required min | Window met | Target behavior seen | Structured failure only | Capability validation status | Primary failure class | Needs rerun |
| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| `task_4_real_gateway_probe` | completed | L3 | yes | 116.07 | 90 command / 140 ready | command yes, ready no | Gateway command attempt/success | no | partial: command telemetry validated; completed Gateway not validated | insufficient_duration | yes, if validating ready Gateway |
| `task_6_real_cyber_core_probe` | completed | L3 | yes | 116.07 | 180 | no | no Assimilator/Cyber Core attempt or success | yes: `gateway_not_ready` | not_validated | insufficient_duration | yes |
| `task_8_real_combat_unit_production_probe` | completed | L3 | yes | 116.07 | 200 | no | no combat-unit attempt or success | yes: `gateway_not_ready` | not_validated | insufficient_duration | yes |
| `task_10_real_attack_defend_probe` | completed | L3 | yes | 116.07 | 220 | no | `defend_order` telemetry, but `own_army_count=0` | yes: no friendly army | not_validated for real army orders | missing_prerequisite | yes |
| `task_12_real_combat_event_probe` | completed | L3 | yes | 116.07 | 240 | no | enemy-visible combat signal | yes for friendly combat: no army | telemetry_diagnostic_validated; friendly combat not_validated | combat_not_reached | yes |
| `task_13_phase_b_small_eval` | completed | L3 | yes, 8 matches | 116.07 each | 240 | no | Gateway command and defensive/combat-signal telemetry | yes: no army | not_validated as playable baseline eval | insufficient_duration | yes |
| `task_14_phase_b_report` | completed | L3 | uses task 13 real data | 116.07 each | 240 | no | report correctly says Level 1 not reached | n/a | diagnostic_report_validated; capability not_validated | insufficient_duration | regenerate after rerun |
| `task_15_phase_b_closeout` | completed | L3 | uses Phase B evidence | 116.07 each | 240 | no | closeout correctly blocks Phase C | n/a | diagnostic_closeout_validated; Phase B capability not accepted | insufficient_duration | update after rerun |

## Task Details

### task_4_real_gateway_probe

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: partial
- minimum_opportunity_window_met: partial
- actual_game_time: 116.07
- required_min_game_time: 90 for command telemetry; 140 for ready Gateway
- primary_failure_class: insufficient_duration for ready Gateway validation
- evidence_quality: real L3 artifact evidence, command-only
- needs_rerun_after_window_fix: yes, if the acceptance target is Gateway ready
- evidence path:
  `data/logs/evaluation/phase_b_task4_gateway_probe/reallaunch-05627d9a/`

Observed:

- `gateway_build_attempt=1`
- `gateway_build_success=1`
- command issued at `game_time=90.0`
- match ended at `game_time=116.07`

### task_6_real_cyber_core_probe

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: not_validated
- minimum_opportunity_window_met: false
- actual_game_time: 116.07
- required_min_game_time: 180
- primary_failure_class: insufficient_duration
- evidence_quality: real L3 artifact evidence, structured skip only
- needs_rerun_after_window_fix: yes
- evidence path:
  `data/logs/evaluation/phase_b_task6_cyber_core_probe/reallaunch-619366ed/`

Observed:

- `assimilator_build_skipped=651`, last reason `gateway_not_ready`
- `cybernetics_core_build_skipped=651`, last reason `gateway_not_ready`
- no Assimilator/Cyber Core attempt or success.

### task_8_real_combat_unit_production_probe

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: not_validated
- minimum_opportunity_window_met: false
- actual_game_time: 116.07
- required_min_game_time: 200
- primary_failure_class: insufficient_duration
- evidence_quality: real L3 artifact evidence, structured skip only
- needs_rerun_after_window_fix: yes
- evidence path:
  `data/logs/evaluation/phase_b_task8_combat_unit_probe/reallaunch-1aaf5fc8/`

Observed:

- `combat_unit_production_skipped=651`
- last reason `gateway_not_ready`
- `combat_unit_production_attempt=0`
- `combat_unit_production_success=0`

### task_10_real_attack_defend_probe

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: not_validated
- minimum_opportunity_window_met: false
- actual_game_time: 116.07
- required_min_game_time: 220
- primary_failure_class: missing_prerequisite
- evidence_quality: real L3 artifact evidence, no friendly army
- needs_rerun_after_window_fix: yes
- evidence path:
  `data/logs/evaluation/phase_b_task10_attack_defend_probe/reallaunch-fe78a347/`

Observed:

- `army_order=651`
- `defend_order=429`
- `attack_order=0`
- `own_army_count > 0 = 0`

The order telemetry is diagnostic evidence. It is not proof that real units
received attack or defend commands.

### task_12_real_combat_event_probe

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: telemetry_diagnostic_validated; friendly combat not_validated
- minimum_opportunity_window_met: false for friendly combat
- actual_game_time: 116.07
- required_min_game_time: 240
- primary_failure_class: combat_not_reached
- evidence_quality: real L3 artifact evidence, enemy signal only
- needs_rerun_after_window_fix: yes
- evidence path:
  `data/logs/evaluation/phase_b_task12_combat_event_probe/reallaunch-e73a3d90/`

Observed:

- `combat_event_detected=423`
- `combat_event_skipped=228`
- `enemy_combat_unit_nearby=true=423`
- `own_army_count > 0 = 0`

This validates enemy-visible combat-signal telemetry. It does not validate
friendly combat.

### task_13_phase_b_small_eval

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: not_validated
- minimum_opportunity_window_met: false
- actual_game_time: 116.07 for each match
- required_min_game_time: 240
- primary_failure_class: insufficient_duration
- evidence_quality: real multi-match artifact evidence, no playable army
- needs_rerun_after_window_fix: yes
- evidence path:
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`

Observed:

- 8 real matches
- all 8 had result, replay, telemetry
- `gateway_build_success_count=8`
- `combat_unit_production_success_count=0`
- `own_army_positive_event_count=0`
- `attack_order_count=0`
- `Result.Defeat=8`

This is valid small-eval execution evidence. It is not valid playable-baseline
capability evidence.

### task_14_phase_b_report

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: diagnostic_report_validated; gameplay capability not_validated
- minimum_opportunity_window_met: false in source data
- actual_game_time: 116.07 per source match
- required_min_game_time: 240
- primary_failure_class: insufficient_duration
- evidence_quality: report correctly states Level 1 not reached
- needs_rerun_after_window_fix: yes, regenerate after rerun
- evidence path:
  `artifacts/reports/phase_b_playable_competitive_core/report.md`

The report is valid because it does not claim Level 1. It should not be used as
evidence that the bot is playable.

### task_15_phase_b_closeout

- task_status: completed
- diagnostic_status: completed
- capability_validation_status: diagnostic_closeout_validated; Phase B capability not accepted
- minimum_opportunity_window_met: false in source data
- actual_game_time: 116.07 per source match
- required_min_game_time: 240
- primary_failure_class: insufficient_duration
- evidence_quality: closeout correctly blocks Phase C
- needs_rerun_after_window_fix: yes, update after rerun
- evidence path:
  `docs/handoffs/latest.md`

The closeout is valid as a limitation record. Phase B should not be considered
accepted as a playable competitive core.

## Error Patterns Found

Confirmed:

- structured failure reason was sometimes treated as L3 task completion;
- L3 task completion was too easy to read as capability validation;
- no-army small eval was completed as evaluation execution, but not as playable
  capability;
- enemy-visible combat telemetry was recorded, but friendly combat was not
  reached.

Corrected interpretation:

- `completed` means the task ran and evidence was collected;
- `diagnostic_status=completed` means the artifact/telemetry diagnostic is
  useful;
- `capability_validation_status=not_validated` means the gameplay capability was
  not demonstrated.

## Current Phase B Acceptance

Phase B is not accepted as a playable competitive core.

Phase B is accepted only as diagnostic/evidence infrastructure for identifying
the next blocker.

## Recommended Next Task

Create a focused Phase B follow-up queue before Phase C:

1. raise or parameterize the real-match duration window for Phase B capability
   probes;
2. rerun Gateway-ready / Cyber Core / combat-unit production probes;
3. only after real combat units exist, rerun attack/defend and combat probes;
4. regenerate the Phase B small eval and report;
5. reassess Level 1.

Fix order:

1. duration window first;
2. then production logic if longer windows still do not produce units.
