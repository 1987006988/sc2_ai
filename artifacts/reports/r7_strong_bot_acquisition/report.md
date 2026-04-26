# R7 Strong Bot Acquisition Report

Date: 2026-04-27

## Executed Tasks

- `r7_task_004_acquire_and_license_audit_selected_strong_bot`
- `r7_task_005_run_selected_strong_bot_and_collect_seed_data`

## Selected Candidate

- candidate:
  - `distar_zvz_agent_platform`
- source:
  - `https://github.com/opendilab/DI-star`
- acquired path:
  - `third_party/strong_bots/DI-star`
- commit:
  - `12b1c69350ad41e17895c602a66a52d98dd58452`

## License Audit

- repository license:
  - Apache-2.0
- audit result:
  - permissive for research use
- unresolved blocker:
  - none for source acquisition and teacher-data use

## Role Classification

- accepted role for this checkpoint:
  - `teacher`
- bounded secondary role:
  - `substrate_candidate`
- why not full substrate acceptance yet:
  - this turn did not install the legacy DI-star runtime stack
  - this turn did not run a local DI-star match
  - the runtime path is documented, but direct execution is deferred

## Dependency and Run Audit

Repository evidence shows:

1. `README.md` documents:
   - `agent_vs_agent`
   - `agent_vs_bot`
   - pretrained model download flow
2. `docs/installation.md` documents:
   - packaged Windows play flow
   - replay-based SC2 4.10.0 activation flow
3. `setup.py` documents:
   - installable python package
   - explicit dependency list
4. `data/replays/` exists in the acquired source

## Seed Data Result

This turn used the repository-provided replay corpus as the valid seed data
materialization path.

- materialized manifest:
  - `data/r7/strong_bot_seed/manifest.json`
- replay count:
  - `16`
- replay versions:
  - `4.10.0` through `5.0.8`

This is sufficient to support teacher-data feasibility for the next phase.

## Gate Judgement

### `r7_task_004`

- minimum gate:
  - `passed`
- target gate:
  - `passed`
- stretch gate:
  - `failed`

Reason:

- source is acquired and version-pinned
- license is audited
- run instructions and dependency path are documented
- no backup candidate was acquired in this turn

### `r7_task_005`

- minimum gate:
  - `passed`
- target gate:
  - `passed`
- stretch gate:
  - `failed`

Reason:

- a valid replay corpus was materialized and pinned
- provided data is rich enough to support later action/state extraction work
- no direct local run or strength comparison was executed in this turn

## What This Proves

1. the project has acquired one strong candidate legally and reproducibly
2. the selected source is viable as a teacher input for R7
3. the project can move into teacher-data materialization without reopening R6

## What This Does Not Prove

1. it does not prove DI-star already runs locally in this repository environment
2. it does not prove online substrate intervention is ready
3. it does not prove stronger-than-baseline outcome on this machine

## Post-Acquisition Repair Update

The later R7.4 online repair work showed that DI-star should remain the accepted
teacher-first source, but should no longer be treated as the preferred online
substrate on this local SC2 stack.

Replacement substrate candidate selected during the R7.4 repair path:

- candidate:
  - `sludge_revived_current_patch_house_bot`
- source:
  - `https://github.com/aiarena/sludge-revived`
- acquired path:
  - `third_party/strong_bots/sludge-revived`
- commit:
  - `9703a799456751d6bba1fdbaf0c799636dddb7af`
- license:
  - MIT
- audit result:
  - permissive for research use

Why this replacement is preferred for the online substrate role:

1. repository README states support for Python 3.11
2. repository README states support for SC2 patch 5.0.13
3. repository is maintained under the AI Arena organization for housebot usage
4. source-level advisor insertion is materially simpler than the DI-star runtime
   path

What later became true in the R7.4 repair path:

1. `sludge-revived` passed a local runtime smoke on this machine with replay save
2. advisor-wrapped A/B/C arms were integrated on that substrate
3. an accepted online internal slice now exists at:
   - `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/summary.json`

What is still missing after that later repair:

1. no external bot-ecosystem validation has been accepted yet
2. no broader multi-slice online robustness claim exists yet
