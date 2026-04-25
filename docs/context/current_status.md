# Current Status

## Execution Sync Status

As of 2026-04-25, the active execution state is:

- active queue:
  - `docs/plans/active/research_master_task_queue.yaml`
- latest handoff:
  - `docs/handoffs/latest.md`
- current active next task:
  - `project_core_goal_reached`

Latest checkpoint state:

- `checkpoint_F_adaptive_research_gate`
  - `minimum_gate_passed = true`
  - `target_gate_passed = true`
  - `decision = accepted_continue`
  - `failure_class = none`

Latest completed task state:

- `task_017_null_vs_adaptive_paired_evaluation`
  - invalid polluted control output was excluded from final judgment
  - accepted control slice reached `1/3` wins
  - accepted retuned treatment slice reached `2/3` wins
  - accepted behavior delta concentrated on `continue_scouting` persistence
  - one adaptive research contribution is now accepted on a matched Easy Zerg
    slice

Repository sync check:

- local `HEAD` and `origin/main` were verified as aligned during the latest
  sync audit;
- the active queue, latest handoff, and latest checkpoint report must be kept
  in sync together when pushing future updates;
- later pushes must not update only a report or only a handoff while leaving
  the queue in an older state.

## Research Control Files

The first-round GPT Pro core control files were imported from `docs/pro.txt` on
2026-04-24. The second-round execution-recipe files were imported from
`docs/pro2.txt` on 2026-04-24. Together they now form the complete active
research control layer:

- `docs/foundation/04_research_direction/research_direction_decision.md`
- `docs/foundation/04_research_direction/retain_rewrite_drop_matrix.md`
- `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `docs/experiments/real_match_validation_protocol.md`
- `docs/plans/active/phase_playable_core_rebuild.md`
- `docs/plans/active/phase_adaptive_response_research.md`
- `docs/experiments/checkpoint_acceptance_spec.md`
- `docs/agents/codex_execution_rules_research_mode.md`
- `docs/templates/task_recipe_template.md`
- `docs/experiments/failure_repair_playbook.md`

Import status:

- first_round_imported: complete
- second_round_imported: complete
- partial_imported: none

Current source-of-truth status:

- upgraded from candidate draft set to complete control layer;
- old active-plan files remain in the repository as historical background only;
- old phase queues and manual triggers are no longer execution authority;
- the next allowed execution entrypoint is
  `docs/plans/active/research_master_task_queue.yaml`.

Control-layer cleanup status:

- the new control layer has been fully imported and cleaned up;
- old plans have been explicitly downgraded to historical reference;
- the repository may now begin from the new master queue;
- this round added no new gameplay capability and only clarified governance.

Legacy/historical plan separation is indexed in:

- `docs/plans/legacy_index.md`

## Phase

Phase 1D and Phase 1E foundation work is complete. Phase 1F demo packaging and standalone Phase L0 execution planning are paused.

The active route is now the research control layer centered on
`docs/plans/active/research_master_task_queue.yaml`.

Current accepted milestone state:

- Level 1 playable baseline is accepted through
  `checkpoint_E_level1_baseline_gate`
- one adaptive research contribution is accepted through
  `checkpoint_F_adaptive_research_gate`
- the accepted adaptive result is bounded to one matched Easy Zerg slice and is
  not yet a broader-pool extension claim

## Mainline

The bot is still a minimal survival baseline, not a strategy bot. It now:

- builds enriched live `GameState` snapshots from python-sc2;
- records enriched `ScoutingObservation` telemetry for opponent-model inputs;
- dispatches one worker scout to create real enemy observations;
- trains workers when safe and affordable;
- sustains Protoss supply with minimal pylon placement;
- exits by structured runtime limits.

## Evaluation

Smoke evaluation now runs a minimal local dry-run loop and persists:

- match result;
- replay metadata placeholder;
- telemetry path;
- evaluation summary.

The project also supports SC2PATH-based runtime preflight and a real local-match validation branch. On this machine, the repository can now:

- resolve `SC2PATH`;
- validate real installed maps under `D:\games\StarCraft II\Maps`;
- launch a real local SC2 match through python-sc2;
- save a replay, telemetry, match result, and replay metadata.
- keep the real local match bot loop alive until a minimal sustained runtime window instead of exiting after the first probe step.
- run a small real built-in opponent batch and summarize per-match status, duration, replay path, and opponent metadata.
- run null vs rule-based opponent-model ablation and generate JSON/Markdown reports.
- validate `opponent_prediction` telemetry in real SC2 local matches for both
  null and rule_based modes.
- run null vs rule_based prediction-only vs minimal_behavior intervention
  comparison on real local SC2 matches and generate Phase 1E JSON/Markdown
  reports.

## Research

Research directories are isolated and contain no production dependencies.

## Current Priority

- keep the research control layer as the only execution authority;
- keep queue / handoff / checkpoint report synchronized when pushing updates;
- treat old Phase A / Phase B / Phase B-R plans and queues as historical
  context, not as current task sources;
- treat the core project goal as reached at the current planned scope;
- if work continues, treat it as extension work beyond the accepted core goal,
  not as unfinished baseline/adaptive core validation.

## Decisions Landed

- Phase-1 engineering base target: bare python-sc2.
- Ares-sc2 is deferred and not required for phase-1 start.
- Opponent-modeling prototype protocol is established in `research/opponent_modeling/`.
- SC2 root path is expected from `SC2PATH`; local machine example: `D:\games\StarCraft II`.
- Real SC2 process launch validation now works at the executable-launch level.
- AI Arena 2025PS2 maps are installed in `D:\games\StarCraft II\Maps`.
- A real local SC2 match probe now runs through python-sc2 and saves a replay.
- The real local bot loop now exits on a sustained `game_loop` limit rather than a one-iteration probe limit.
- WSL can invoke Windows PowerShell and Windows Python to launch the Windows SC2 install for real local-match validation.
- Phase 1C real validation produced non-empty enemy observations from live scouting.
- The local built-in opponent pool now includes Terran Easy, Terran Medium, Zerg Easy, and Protoss Easy.
- Phase 1D ablation v0 runs null vs rule_based configs across a small fixed opponent pool.
- Rule-based opponent model v0 is prediction-only and records risk signals without changing gameplay.
- Feature extraction and report generation now produce `artifacts/reports/phase1d_ablation_opponent_model/summary.json` and `report.md`.
- The corrected Phase 1D queue now distinguishes L1 synthetic tests, L2 dry
  telemetry, and L3 real telemetry; task 6b produced real `opponent_prediction`
  telemetry under `data/logs/evaluation/phase1d_task6b_probe/reallaunch-f4b16b51/`.
- Phase 1D closeout validated:
  - null real match: `data/logs/evaluation/phase1d_task11a_null_match/reallaunch-b111cf67/`;
  - rule_based real match: `data/logs/evaluation/phase1d_task11b_rule_based_match/reallaunch-edba8ac0/`;
  - 2x2 real ablation batch: `data/logs/evaluation/phase1d_ablation_opponent_model/`;
  - report artifacts: `artifacts/reports/phase1d_ablation_opponent_model/`.
- Phase 1E minimal strategy intervention validated:
  - tag-only real probe:
    `data/logs/evaluation/phase1e_task5_tag_only_probe/reallaunch-350f1ad9/`;
  - minimal_behavior real probe:
    `data/logs/evaluation/phase1e_task7_minimal_behavior_probe/reallaunch-0997c3b4/`;
  - 1 map x 2 opponents x 3 configs real ablation:
    `data/logs/evaluation/phase1e_strategy_intervention_ablation/20260421T145911Z/`;
  - report artifacts:
    `artifacts/reports/phase1e_strategy_intervention/summary.json` and
    `artifacts/reports/phase1e_strategy_intervention/report.md`.
- Project roadmap recalibrated on 2026-04-21:
  - Phase 1D/1E are foundation milestones for runtime, telemetry, prediction,
    strategy-response telemetry, reporting, and L3 validation;
  - they are not final demo milestones and do not prove ladder readiness;
  - Phase 1F demo packaging is paused until a ladder-ready playable core exists;
  - the active roadmap is Ladder-Ready Adaptive SC2 Bot Roadmap, starting with
    Phase L0 Ladder Readiness.
- Project roadmap recalibrated again on 2026-04-22:
  - the active goal is now Ladder-Competitive Adaptive SC2 Bot Plan;
  - ladder readiness is a foundation, not the project ceiling;
  - each smallest Codex task should fit one Plus 5-hour quota window, but the
    whole project is not limited to one window;
  - target levels now run from Level 0 real match data foundation through Level
    5 learning-augmented research modules;
  - interview showcase target is at least Level 3 opponent-adaptive behavior,
    preferably Level 4 opponent-pool evaluation.
- Phase A closed out on 2026-04-22 as infrastructure/data foundation:
  - A1 infrastructure gate report:
    `artifacts/reports/phase_a_ladder_infra_dataset/a1_infrastructure_gate/summary.json`;
  - merged Baseline Dataset V0 manifest:
    `data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json`;
  - baseline quality report:
    `artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/summary.json`;
  - scalable collection config levels:
    `configs/evaluation/phase_a_collection_levels.yaml`;
  - Baseline V0 contains 24 real match attempts across 2 maps, 3 races, and
    Easy/Medium built-in opponents, with result/replay/telemetry present for
    all matches.
- Phase B task queue completed on 2026-04-22 with real evidence but did not
  reach Level 1 playable baseline:
  - Phase B report:
    `artifacts/reports/phase_b_playable_competitive_core/report.md`;
  - Phase B summary:
    `artifacts/reports/phase_b_playable_competitive_core/summary.json`;
  - small real eval source run:
    `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`;
  - 8 real matches completed with result/replay/telemetry artifacts;
  - Gateway build success count was 8;
  - combat-unit production success count was 0;
  - no telemetry event reported `own_army_count > 0`;
  - attack order count was 0;
  - all 8 matches ended as `Result.Defeat`.
- Phase B evidence audit on 2026-04-22:
  - audit report:
    `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`;
  - all audited probes and small-eval matches ended around
    `game_time=116.07`;
  - cutoff source was bot self-exit in `src/sc2bot/runtime/game_loop.py`,
    controlled by `configs/bot/debug.yaml` with
    `runtime.max_game_loop: 2600`;
  - this is `insufficient_duration` for Gateway-ready, Cyber Core,
    combat-unit production, real army orders, and friendly combat validation;
  - task completion and diagnostic evidence are now explicitly separated from
    gameplay capability validation;
  - Phase B is not accepted as a playable competitive core and should not enter
    Phase C until follow-up L3 probes rerun after the duration-window fix.
- Phase B-R revalidation planning created on 2026-04-22:
  - plan:
    `docs/plans/active/phase_b_revalidation_playable_core.md`;
  - task queue:
    `docs/plans/active/phase_b_revalidation_task_queue.yaml`;
  - manual trigger:
    `docs/plans/active/phase_b_revalidation_manual_trigger.md`;
  - checkpoints are mandatory every three tasks;
  - each capability task has minimum, target, and stretch gates;
  - Phase C remains blocked until Phase B-R final checkpoint accepts the
    original playable-core objective.

## Blockers

- The bot still does not have a real build order, combat plan, expansion logic, gas/tech progression, or production-informed behavior.
- Current opponent observations depend on a single worker scout and are enough for input-stream validation, not robust scouting.
- Current Phase 1D ablation is prediction-only; it validates the experiment
  chain but does not demonstrate improved gameplay or win rate.
- Current Phase 1E intervention is intentionally thin; it validates response-tag
  and minimal behavior telemetry, not strategic quality or win-rate improvement.
- Phase A validates local ladder-like infrastructure and dataset collection,
  but not ladder competitiveness.
- Phase B established real small-eval reporting and Gateway command telemetry,
  but not a playable competitive core.
- Phase B capability validation is blocked by insufficient real-match duration:
  current probes end at about 116.07 game seconds due `runtime.max_game_loop:
  2600`, before Cyber Core, combat-unit production, attack/defend, and friendly
  combat can be fairly validated.
- No real combat-unit production succeeded in the Phase B small eval.
- No baseline win against built-in Easy/Medium has been established.
- Baseline V0 all ended with `max_game_time_reached`; this is expected for the
  current survival scaffold but does not demonstrate strength.
