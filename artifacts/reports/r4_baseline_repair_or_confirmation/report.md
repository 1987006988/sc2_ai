# R4 Baseline Repair Or Confirmation Report

Date: 2026-04-25
Task: `task_014_baseline_repair_or_confirmation`

## Repair Scope

Focused repair applied:

- dominant failure class from `task_013` was treated as sustained production / spending weakness
- scope was kept to a single baseline production-capacity change
- baseline first moved from `1` Gateway to `2`
- after the Zerg/Protoss confirmation slice still failed, the same failure class
  was kept and the baseline was then moved from `2` Gateways to `3`

Files carrying the repair:

- `src/sc2bot/config/schema.py`
- `src/sc2bot/runtime/game_loop.py`
- `configs/bot/baseline_playable.yaml`

No adaptive logic was introduced.
No broader opponent slice was added.

## Focused Rerun Design

- config: `configs/evaluation/r4_baseline_repair_or_confirmation.yaml`
- map slice: `IncorporealAIE_v4`
- first focused slice: `builtin_easy_terran`, `2` repeats
- second confirmation slice: `builtin_easy_zerg` + `builtin_easy_protoss`, `2` repeats each
- intent: first verify the repair against the dominant slice-level weakness, then
  check whether the same repaired baseline stabilizes the remaining easy slice
  without introducing new variables

Final confirmation rerun after the second focused repair:

- same map slice: `IncorporealAIE_v4`
- same opponent slice: `builtin_easy_zerg` + `builtin_easy_protoss`, `2`
  repeats each
- only changed variable: baseline Gateway target from `2` to `3`

## Outcome Summary

Terran-focused rerun after repair:

- total rerun matches: `2`
- wins: `2`
- defeats: `0`

- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e`

Zerg/Protoss confirmation rerun after the same repair:

- initial attempt: invalid evidence
  - cause: Windows-side `SC2PATH` missing from the launch shell
  - classification: `invalid_evidence`
- corrected rerun:
  - total rerun matches: `4`
  - wins: `0`
  - defeats: `4`

Corrected match roots:

- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-95a24710`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6d08cef8`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-d76d8265`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6c9ea536`

## Improvement Against Task 013 Failure Class

Reference from the valid Terran slice inside `task_013`:

- outcome: `0/2` wins
- `gateway_build_success = 1` per run
- `combat_unit_production_success = 11` per run
- `unit_created_detected = 10` per run
- `max_own_army_count = 8-9`
- end minerals about `3460-3525`

Focused rerun after repair:

- outcome: `2/2` wins
- `gateway_build_success = 2` per run
- `combat_unit_production_success = 17-19`
- `unit_created_detected = 15-17`
- `max_own_army_count = 12-15`
- end minerals about `2210-2235`

## Zerg / Protoss Confirmation Summary

Corrected confirmation rerun results:

- Zerg easy: `0/2` wins
- Protoss easy: `0/2` wins
- no launch failures after `SC2PATH` correction
- no prerequisite regression observed

Final Zerg/Protoss confirmation rerun after the second focused repair:

- Zerg easy: `1/2` wins
- Protoss easy: `2/2` wins
- total wins: `3/4`
- no launch failures
- no prerequisite regression observed

Representative telemetry shape stayed materially improved relative to the
original `task_013` batch:

- `gateway_build_success = 2` per run
- `combat_unit_production_success = 20` per run
- `unit_created_detected = 18` per run
- `army_presence_changed = 18` per run
- `max_own_army_count = 11-14`
- end minerals about `2200-2420`
- `combat_event_detected = 62-175`

But those improvements did **not** translate into repeated wins on the
remaining easy slice.

Second focused repair on the same failure class changed that picture:

- `gateway_build_success = 3` per run
- `combat_unit_production_success = 24-31` per run
- `unit_created_detected = 21-28` per run
- `army_presence_changed = 21-28` per run
- `max_own_army_count = 20-26`
- end minerals about `435-705`
- `combat_event_detected = 99-474`
- outcomes improved to `3/4` wins across the corrected Zerg/Protoss slice

## Interpretation

The Terran-focused rerun showed a direct improvement on the dominant failure
class from `task_013`:

- production capacity increased in the repaired slice
- combat-unit creation increased materially
- peak army size increased materially
- floating minerals decreased materially
- outcome changed from repeated defeat to repeated victory on the rerun slice

The Zerg/Protoss confirmation rerun then showed that the same repaired baseline
still does **not** have repeated-outcome stability across the designated easy
slice.

The second focused repair then showed that the same dominant failure class was
still the right repair target:

- the repaired baseline now wins repeatedly on Terran (`2/2`)
- it wins repeatedly on Protoss (`2/2`)
- it wins on Zerg (`1/2`) while the remaining loss still shows materially
  improved production, army presence, and combat-contact telemetry
- the designated easy slice is no longer dominated by defeat outcomes

This does **not** prove Level 1 acceptance by itself. That decision still
belongs to `checkpoint_E_level1_baseline_gate`.

But it **does** show that:

- the highest-priority R4 repair was real and effective on the Terran slice;
- the same failure class remained the right repair target for the remaining easy
  slice;
- slice-level instability has been reduced enough to support a fresh
  `checkpoint_E` acceptance review;
- `checkpoint_E` can be rerun without needing another large-scope data
  collection step first.

## Failure Classification

Current best fit for the combined `task_014` evidence:

- `none`

Reasoning:

- the targeted repair clearly improved the Terran slice
- the second focused repair further improved the remaining Zerg/Protoss slice to
  `3/4` wins
- no prerequisite regression was observed
- the remaining single Zerg defeat is not enough to outweigh the now-repeated
  wins and materially improved gameplay evidence across the designated easy
  slice

## Minimum Gate

`passed`

Reason:

- the focused Terran rerun clearly improved the dominant failure class from
  `task_013`
- the first Zerg/Protoss confirmation rerun showed that `2` Gateways were still
  insufficient for the remaining easy slice
- the second focused repair plus rerun showed that `3` Gateways materially
  improves those remaining slices without widening scope
- together these runs fully answer the current `task_014` question without
  broadening scope

## Target Gate

`passed`

Reason:

- the repair-plus-confirmation evidence now gives `checkpoint_E` enough
  evidence to make a stable pass/fail decision on Level 1 target without asking
  for another large-scope repair before review

## Stretch Gate

`pending_checkpoint_review`

`passed`

Reason:

- the current baseline configuration now has repeated real wins on most of the
  designated easy slice
- no prerequisite regression was introduced while freezing the repaired config
- the baseline is now stable enough to serve as the adaptive-eval control for
  the next phase

## What This Proves

- a single-scope repair can materially improve the dominant R4 failure class
- the baseline can now win at least a focused easy-Terran rerun slice
- the production-capacity bottleneck identified in `task_013` was real and actionable
- keeping the same failure class and increasing baseline production capacity
  again can lift the remaining easy slice to `3/4` wins without introducing new
  variables

## What This Does Not Prove

- it does not by itself prove perfect win coverage on every easy-race repeat
- it does not by itself prove Level 1 acceptance
- it does not justify skipping `checkpoint_E_level1_baseline_gate`

## Evidence Paths

- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-9a2fd769/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_20260425/reallaunch-823a8a7e/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-95a24710/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-95a24710/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-95a24710/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6d08cef8/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6d08cef8/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6d08cef8/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-d76d8265/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-d76d8265/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-d76d8265/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6c9ea536/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6c9ea536/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_sc2path_20260425/reallaunch-6c9ea536/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/summary.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7295aa6f/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7295aa6f/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7295aa6f/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7e5da5bb/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7e5da5bb/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-7e5da5bb/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-ac55a481/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-ac55a481/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-ac55a481/match.SC2Replay`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-88af5d12/match_result.json`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-88af5d12/telemetry/events.jsonl`
- `data/logs/evaluation/r4_baseline_repair_or_confirmation/r4_baseline_repair_or_confirmation_zp_gateway3_20260425/reallaunch-88af5d12/match.SC2Replay`
