# Phase B-R: Playable Competitive Core Revalidation

Status: planned.

Task queue: `docs/plans/active/phase_b_revalidation_task_queue.yaml`

Manual trigger: `docs/plans/active/phase_b_revalidation_manual_trigger.md`

## Purpose

Phase B-R exists because the original Phase B task queue was exhausted without
validating the original Phase B objective. The queue produced useful diagnostic
evidence, but task completion was not equivalent to gameplay capability
validation.

## Original Phase B Review

Original goal:

- make the Protoss bot a playable baseline that can build, produce combat
  units, defend, attack, and run against defined baseline opponents;
- make real gameplay behavior, replay quality, build progression,
  combat-unit production, army orders, and combat telemetry core acceptance
  criteria;
- avoid ladder-competitiveness claims.

Original done criteria:

- the bot repeatedly completes basic Protoss build progression when not
  disrupted;
- the bot produces Zealots and/or Stalkers;
- the bot defends own base and attacks known enemy base;
- combat telemetry records engagements, units killed/lost where available, and
  defend/attack commands;
- the bot has measured outcomes against built-in Easy/Medium without
  overclaiming beyond the data.

Original closeout gate:

- Gateway real probe reaches L3;
- Assimilator/Cybernetics Core real probe reaches L3;
- combat-unit production real probe reaches L3;
- attack/defend order real probe reaches L3;
- combat event real probe reaches L3, or records a clear structured reason for
  no combat;
- Phase B small real evaluation reaches L3;
- Phase B report uses real match data;
- report states whether current data shows wins against built-in Easy/Medium;
- report does not claim ladder competitiveness.

Current Phase B state:

- task queue exhausted;
- objective not accepted;
- playable baseline not reached;
- Level 1 not reached;
- Phase C blocked.

## Why Original Phase B Failed

Evidence audit:

- `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`

Root cause:

- audited real probes and the 8-match small eval ended around
  `game_time=116.07`;
- cutoff was bot self-exit from `src/sc2bot/runtime/game_loop.py`;
- controlling config was `configs/bot/debug.yaml`;
- controlling value was `runtime.max_game_loop: 2600`;
- this was below the minimum opportunity window for Gateway-ready, Cyber Core,
  combat-unit production, real army orders, and friendly combat.

Diagnostic-only evidence:

- Gateway command telemetry appeared, but Gateway-ready/completion was not
  fairly validated;
- Assimilator/Cyber Core telemetry was structured skip evidence, not capability
  validation;
- combat-unit production telemetry was structured skip evidence, not production
  validation;
- attack/defend telemetry was not valid real army-order evidence because
  `own_army_count` stayed zero;
- combat-signal telemetry was enemy-visible diagnostic evidence, not friendly
  combat validation;
- small eval execution was valid as diagnostic evidence, not playable-baseline
  capability evidence.

Phase C cannot start because Phase C requires a playable core whose behavior
can be adapted. The current evidence does not validate friendly army,
attack/defend, combat, or baseline outcomes.

## Goal

Revalidate and complete the original Phase B objective at a stricter evidence
standard:

- Protoss bot completes basic build progression;
- bot reliably produces combat units;
- bot rallies army;
- bot defends;
- bot attacks;
- bot produces real friendly combat telemetry;
- bot runs real multi-match evaluation on built-in Easy / Medium;
- bot reaches at least Level 1 playable baseline;
- no ladder-competitiveness claim is made.

## Non-Goals

- No expansion strategy.
- No advanced tech beyond the minimum Cybernetics Core path.
- No upgrades.
- No complex army composition.
- No SMAC.
- No LLM.
- No replay learning.
- No learned opponent model.
- No combat predictor.
- No league/self-play.
- No opponent-adaptive claims before Phase C.
- No ladder-competitiveness claim.

## Acceptance Philosophy

Do not set the plan target to the minimum passing standard.

Every capability task has:

- minimum gate: the lowest result required to continue;
- target gate: the planned successful outcome;
- stretch gate: optional upside if time and stability allow.

`completed` is not the same as `accepted`.

`diagnostic completed` is not the same as `capability validated`.

Structured failure reasons are useful diagnostics, but they are not capability
success unless the checkpoint explicitly accepts that class of result.

## Checkpoint Cadence

Every third task is a checkpoint:

- `task_3_checkpoint_A_duration_window_acceptance`
- `task_6_checkpoint_B_build_chain_acceptance`
- `task_9_checkpoint_C_production_acceptance`
- `task_12_checkpoint_D_tactical_acceptance`
- `task_15_checkpoint_E_phase_b_acceptance`

If a checkpoint decision is not `accepted_continue`, later tasks must not run.
The next action must be a repair, split, or blocked-state update.

## Opportunity Windows

Initial required minimum opportunity windows:

- Gateway command: 90s
- Gateway ready: 140s
- Assimilator / Cyber Core: 180s
- Combat-unit production: 220s
- Friendly army order: 260s
- Friendly combat: 300s
- Small eval playable baseline: at least 300s per match unless the game ends
  naturally.

If `actual_game_time < required_min_game_time`, the task cannot claim
production or combat failure. It can only classify the result as
`insufficient_duration`.

### Window Contract

The opportunity window is a fairness guard for capability validation. It does
not prove the capability by itself.

| Capability | Required minimum game time | What can be judged before the window | What cannot be judged before the window |
| --- | ---: | --- | --- |
| Gateway command | 90s | Whether a build command attempt was issued | Gateway completion / tech progression |
| Gateway ready | 140s | Gateway command telemetry and structured placement/resource failures | Whether Gateway-ready production path works |
| Assimilator / Cyber Core | 180s | Whether prior Gateway path blocks tech progression | Whether gas / Cyber Core logic works |
| Combat-unit production | 220s | Whether production was skipped because prerequisites were missing | Whether Zealot/Stalker production works |
| Friendly army order | 260s | Whether empty-order diagnostics are emitted | Whether tactical orders work with real army units |
| Friendly combat | 300s | Enemy-visible combat-signal telemetry | Whether friendly army engages or survives combat |
| Small eval playable baseline | 300s per match unless natural end | Infrastructure stability and artifact persistence | Playable-baseline capability or Level 1 outcome |

### Validation Semantics

Capability validation requires all of the following:

1. `actual_game_time >= required_min_game_time`, unless the game ended naturally.
2. Required artifacts exist: `match_result.json`, replay if gameplay started,
   and `telemetry/events.jsonl`.
3. The target behavior appears in telemetry or a checkpoint explicitly accepts
   a structured blocker as the outcome for that task.
4. Evidence paths are recorded in the active task queue and handoff.

If the time window is insufficient:

- `capability_validation_status: not_validated`
- `failure_class: insufficient_duration`
- the task may still be diagnostically useful;
- the task may not unlock downstream capability tasks.

If the time window is sufficient but the behavior is absent:

- use a specific failure class such as `missing_prerequisite`,
  `production_logic_failure`, `order_logic_failure`, `combat_not_reached`, or
  `unknown`;
- do not call the capability accepted;
- checkpoint must decide whether to repair, split, or block.

### Failure Classes

- `insufficient_duration`: actual game time was below the required opportunity
  window.
- `launch_failure`: SC2 did not enter gameplay.
- `artifact_missing`: required result, replay, telemetry, or summary artifact is
  missing.
- `missing_prerequisite`: a required earlier capability, such as Gateway-ready
  or friendly army, is absent.
- `production_logic_failure`: prerequisites are present, but production does not
  attempt or succeed.
- `order_logic_failure`: friendly army exists, but tactical orders do not issue
  correctly.
- `combat_not_reached`: friendly army and sufficient time exist, but no
  engagement occurs.
- `unknown`: evidence is insufficient to classify more specifically.

## Phase B-R Gates

Minimum Phase B-R acceptance:

- duration blocker resolved;
- friendly army appears in real match telemetry;
- attack/defend appears with `own_army_count > 0`;
- small eval has real gameplay evidence;
- report uses real match data.

Target Phase B-R acceptance:

- built-in Easy pool has repeated wins or clearly quantified near-win
  build/combat indicators;
- Level 1 decision is explicit and evidence-backed.

Stretch Phase B-R acceptance:

- Medium opponent matches have usable result/combat/build records;
- early win/loss matrix exists without claiming ladder competitiveness.
