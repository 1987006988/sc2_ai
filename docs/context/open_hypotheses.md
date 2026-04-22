# Open Hypotheses

## H1: Bare python-sc2 can support the first real local SC2 runtime integration

Status: validated.

Validation:
- verify package availability from the chosen environment source;
- launch a real local SC2-backed bot path;
- check local match orchestration compatibility.

## H2: A simple rule-based opponent model can improve fixed-pool outcomes

Status: mechanism partially validated; outcome improvement remains open.

Validation:
- define fixed opponent pool;
- compare no model vs rule-based model;
- track rush defense and strategy selection metrics.

Current evidence:
- null vs rule_based config switching works;
- rule_based predictions and risk signals are recorded;
- L3 real local matches validated `opponent_prediction` telemetry for both
  null and rule_based modes;
- a real 2x2 null vs rule_based ablation produced report artifacts under
  `artifacts/reports/phase1d_ablation_opponent_model/`;
- Phase 1E validated real `strategy_response`, `strategy_switch`, and
  `minimal_behavior_intervention` telemetry;
- Phase 1E report artifacts exist under
  `artifacts/reports/phase1e_strategy_intervention/`;
- the intervention is intentionally thin, so no win-rate or outcome improvement
  claim is supported yet.

Next validation:
- Do not use Phase 1F packaging as the next validation step.
- First complete Phase A ladder infrastructure/dataset and Phase B playable
  competitive core, then revisit opponent-model impact in Phase C with behavior metrics
  such as attack timing, defend posture, scout persistence, and adaptation count.

## H3: Minimal telemetry is sufficient for first opponent-modeling prototype

Status: validated for v0 telemetry extraction.

Validation:
- log scouting events, strategy switches, and match outcome;
- extract features without replay parsing.

Current evidence:
- live `game_state` and `scouting_observation` telemetry now includes enemy units, enemy structures, first/last seen times, and confidence fields;
- Phase 1D feature extraction generated fixed per-match fields and an ablation report without replay parsing;
- the closeout report paths are
  `artifacts/reports/phase1d_ablation_opponent_model/summary.json` and
  `artifacts/reports/phase1d_ablation_opponent_model/report.md`;
- Phase 1E feature extraction and reporting generated strategy response and
  intervention metrics without replay parsing.

## H4: A layered hybrid Protoss bot can reach a ladder-competitive baseline

Status: infrastructure and diagnostic Phase B evidence gathered; competitive baseline remains open.

Validation:
- Phase A proves ladder-like entrypoint, package dry-run, multi-match real
  batches, dataset manifests, artifact completeness, and crash/timeout stats;
- Phase B must prove basic Protoss build progression, combat units,
  attack/defend behavior, combat telemetry, and baseline wins against built-in
  Easy before this hypothesis can be considered validated.

Current evidence:
- runtime and telemetry foundation exists from Phase 1D/1E;
- Phase A validated package dry-run, A1 infrastructure reporting, scoped
  multi-match collection, a 24-match real baseline dataset manifest, dataset
  quality reporting, and reusable collection levels;
- Baseline V0 evidence lives under
  `data/logs/evaluation/phase_a_baseline_v0/dataset_manifest.json` and
  `artifacts/reports/phase_a_ladder_infra_dataset/baseline_dataset_v0_quality/`;
- Phase B real small eval evidence lives under
  `data/logs/evaluation/phase_b_small_eval/phase_b_small_eval_20260422/`;
- Phase B report artifacts live under
  `artifacts/reports/phase_b_playable_competitive_core/`;
- Phase B evidence audit lives at
  `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`;
- Gateway command telemetry is partially validated on real matches;
- army-order telemetry and combat-signal telemetry are diagnostic only because
  no friendly army existed in the audited matches;
- audited probes ended around `game_time=116.07`, controlled by
  `configs/bot/debug.yaml` with `runtime.max_game_loop: 2600`, which is below
  the minimum opportunity window for Cyber Core, combat-unit production, real
  army orders, and friendly combat;
- no combat-unit production, friendly army presence, attack-order behavior, or
  baseline win target has been validated yet.

Next validation:
- insert a focused Phase B follow-up to fix or parameterize the real-match
  duration window first, then rerun Gateway-ready, Cyber Core,
  combat-unit production, attack/defend, combat, and small-eval probes before
  creating Phase C.

## H5: Opponent modeling can improve real behavior metrics once a playable core exists

Status: open.

Validation:
- compare null vs opponent_model behavior paths after Phase L1 provides stable
  gameplay;
- measure attack timing, defend posture, scout persistence, and adaptation count;
- keep win-rate conclusions separate unless repeated match data supports them.

Current evidence:
- Phase 1D/1E validate prediction, response tags, minimal intervention telemetry,
  and reporting;
- they do not validate real gameplay improvement or ladder performance.

Next validation:
- defer until Phase C Opponent-Adaptive Strategy.

## H6: Real-match-first evidence discipline will prevent overclaiming

Status: partially validated.

Validation:
- every report distinguishes synthetic, dry-run, single real match, and
  multi-match evidence;
- gameplay claims require real matches;
- stability claims require multi-match batches;
- showcase claims require opponent-pool evaluation.

Current evidence:
- Phase 1D/1E introduced L3 real telemetry validation and explicitly avoided
  win-rate/gameplay-quality claims;
- Phase A reports distinguish infrastructure, dry/config, and real baseline
  dataset evidence;
- Phase A closeout explicitly does not claim bot strength from dry/config or
  dataset-artifact evidence;
- Phase B evidence audit caught a completed-vs-capability validation issue and
  reclassified post-Gateway gameplay tasks as not validated due insufficient
  duration.

Next validation:
- carry the reclassification fields into the Phase B follow-up queue, where
  gameplay capability claims must require both real matches and a satisfied
  minimum opportunity window.
