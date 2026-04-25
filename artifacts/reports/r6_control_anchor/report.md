# R6 Control Anchor Report

Date: 2026-04-26
Task: `r6_task_001_freeze_control_and_claim_contract`

## Core Start-State Confirmation

Confirmed from current accepted core records:

- predecessor queue status: `project_core_goal_reached`
- accepted baseline checkpoint: `checkpoint_E_level1_baseline_gate`
- accepted adaptive checkpoint: `checkpoint_F_adaptive_research_gate`

Read sources:

- `docs/context/current_status.md`
- `docs/handoffs/latest.md`
- `docs/plans/active/research_master_task_queue.yaml`
- `artifacts/reports/checkpoints/checkpoint_E_level1_baseline_gate.md`
- `artifacts/reports/checkpoints/checkpoint_F_adaptive_research_gate.md`

## Frozen Control Anchor

- config path: `configs/bot/baseline_playable.yaml`
- config sha256: `9dd606de9b75a89db1aebf7abec87e2eb8691e562147d975968c6f88cba388ee`
- evidence anchor:
  - `artifacts/reports/checkpoints/checkpoint_E_level1_baseline_gate.md`
- accepted meaning:
  - frozen Level 1 baseline control

## Frozen Comparator Anchor

- config path: `configs/bot/adaptive_research.yaml`
- config sha256: `50b468125297b8bc31ce2c4475a1b8e4f4aa77d2dc5c41a47266718f4c6910c9`
- evidence anchor:
  - `artifacts/reports/checkpoints/checkpoint_F_adaptive_research_gate.md`
- accepted meaning:
  - frozen R5 accepted rule-based adaptive comparator

## Frozen Predecessor Queue

- predecessor queue path:
  - `docs/plans/active/research_master_task_queue.yaml`
- predecessor queue sha256:
  - `a90d659d15892b9a312c712e1a233f60257a8bd4bd8aa1c68d68886e388f38ab`
- rule:
  - predecessor queue remains historical completion record
  - R6 does not reopen or overwrite its accepted conclusions

## Frozen Checkpoint Anchors

- `checkpoint_E_level1_baseline_gate.md`
  - sha256: `6ba9f089d359bb63933ea08a2ffe047ed2b12bcafd523ade5353ff5ad9e42230`
- `checkpoint_F_adaptive_research_gate.md`
  - sha256: `6d69ac0d43bf2b63a27bc93b4e5e985b9ea4938e937b233e987ecad9d63f031f`

## Claim Contract

R6 single-feature boundary:

- learned temporal opponent belief conditioned response surface

Allowed response surface only:

1. continue_scouting / scout budget
2. defensive_posture
3. first_attack_timing
4. bounded production tempo

Forbidden scope:

1. reopening baseline acceptance
2. baseline-core drift during R6 evaluation
3. second research feature
4. full macro rewrite
5. full self-play league training
6. external claim before internal and external R6 checkpoints pass

## Verification

- baseline control hash recorded: yes
- accepted adaptive comparator hash recorded: yes
- predecessor queue left unchanged: yes
- R6 claim boundary explicit: yes

## Dataset Contract Addendum

The first R6 dataset-contract unit is now frozen:

- source manifest:
  - `research/r6_temporal_belief/data/source_manifest.yaml`
- dataset manifest:
  - `research/r6_temporal_belief/data/dataset_manifest.json`
- dataset contract config:
  - `configs/research/r6_dataset_manifest.yaml`
- label schema draft:
  - `configs/research/r6_label_schema.yaml`
- leakage-check skeleton:
  - `research/r6_temporal_belief/datasets/splits.py`

The contract explicitly separates:

- future public replay / benchmark sources for train/val/test
- local accepted replay artifacts for domain-anchor-only use
- internal online eval artifacts as forbidden holdout inputs

The split policy explicitly forbids:

- same-series cross-split leakage
- same-player same-time-window cross-split leakage
- local accepted replay artifacts entering holdout benchmark tables
- internal online eval replays re-entering the same-round holdout

## Gate Result

- minimum gate: `passed`
- target gate: `passed`
- stretch gate: `passed`

Reason:

- at least one dataset-integrity validation command now exists through
  `research/r6_temporal_belief/datasets/splits.py`

## What This Proves

- R6 can start without reopening core acceptance history
- frozen control and frozen comparator are version-pinned
- claim boundary is explicit before any replay dataset or training work begins

## What This Does Not Prove

- it does not prove the dataset is populated yet
- it does not prove benchmark labels are correct yet
- it does not validate any learned temporal model yet
- it does not validate any new online or external result
