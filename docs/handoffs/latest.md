# Handoff: Phase B Evidence Audit / Reclassification

Date: 2026-04-22

## Scope

This handoff records a Phase B evidence audit only.

No gameplay code was changed. No tests were run. No SC2 match was run. Phase C
was not started.

## Audit Result

Confirmed issue: Phase B task `completed` status had been too easy to interpret
as gameplay capability validated.

Corrected interpretation:

- task execution completed: the requested command/artifact/report step ran;
- diagnostic completed: the evidence is useful for debugging or reporting;
- gameplay capability validated: the real match reached a sufficient opportunity
  window and demonstrated the target behavior.

Most post-Gateway Phase B tasks are not capability validated.

## Evidence Audit

Audit report:

- `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`

Queue-level reclassification:

- `docs/plans/active/phase_b_playable_competitive_core_task_queue.yaml`

## Cutoff Diagnosis

All audited Phase B probes and the 8-match small eval ended around
`game_time=116.07`.

Cause:

- primary cutoff: bot self-exit in `src/sc2bot/runtime/game_loop.py`;
- controlling config: `configs/bot/debug.yaml`;
- value: `runtime.max_game_loop: 2600`;
- status in result files: `max_game_time_reached`.

This was not a launch failure, artifact failure, timeout, or SC2 process issue.

## Reclassification Summary

- `task_4_real_gateway_probe`: partial. Gateway command telemetry appeared
  (`gateway_build_attempt` and `gateway_build_success`), but Gateway-ready
  capability is not validated because the match ended before the ready-window.
- `task_6_real_cyber_core_probe`: not capability validated. Structured skip
  only, primary failure `insufficient_duration`.
- `task_8_real_combat_unit_production_probe`: not capability validated.
  Structured skip only, primary failure `insufficient_duration`.
- `task_10_real_attack_defend_probe`: not capability validated. No friendly
  army existed, primary failure `missing_prerequisite`.
- `task_12_real_combat_event_probe`: enemy-visible combat-signal telemetry is
  diagnostic; friendly combat is not validated, primary failure
  `combat_not_reached`.
- `task_13_phase_b_small_eval`: valid multi-match diagnostic evidence, not
  playable-baseline capability evidence.
- `task_14_phase_b_report`: diagnostic report valid; source data does not
  validate gameplay capability.
- `task_15_phase_b_closeout`: diagnostic closeout valid; Phase B capability is
  not accepted.

## Current Decision

Phase B is not accepted as a playable competitive core.

Do not create Phase C yet.

## Recommended Next Step

Create a focused Phase B follow-up queue:

1. Fix or parameterize the real-match duration window for Phase B capability
   probes.
2. Rerun Gateway-ready / Cyber Core / combat-unit production probes.
3. Rerun attack/defend and combat probes only after real friendly army units
   exist.
4. Regenerate Phase B small eval and report.
5. Reassess Level 1 playable baseline.

Fix order:

1. duration window first;
2. then production logic if longer windows still do not produce units.
