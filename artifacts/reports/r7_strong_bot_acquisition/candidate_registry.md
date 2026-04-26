# R7 Strong Bot Candidate Registry

Date: 2026-04-27
Task: `r7_task_002_identify_and_rank_strong_bot_candidates`

## Scope

This registry records auditable strong-bot, teacher-data, and comparator
candidates for R7. This is discovery and ranking only.

Not done in this task:

1. no bot download
2. no vendoring
3. no license-dependent integration
4. no model training
5. no SC2 run

## Ranking Summary

### A1. `sludge_revived_current_patch_house_bot`

- Role:
  - preferred replacement substrate
  - comparator candidate
- Source:
  - `aiarena/sludge-revived`
- License:
  - MIT
- Why it now ranks first for substrate:
  - repository README explicitly states support for Python 3.11
  - repository README explicitly states support for SC2 patch `5.0.13`
  - repository is maintained under the AI Arena organization for housebot usage
  - source is Python and exposes visible local run entrypoints plus a modular bot
    structure, so advisor insertion is much simpler than the DI-star runtime path
- Main risks:
  - local runtime on this machine is not yet validated
  - strength evidence is partly historical and must be rechecked locally
  - replay and teacher-data volume are smaller than DI-star and SC2EGSet

### A2. `distar_zvz_agent_platform`

- Role:
  - teacher
  - substrate candidate
  - comparator
- Source:
  - DI-star GitHub
- License:
  - Apache-2.0
- Why it still ranks highly:
  - strongest already-acquired teacher-first source
  - explicit permissive license
  - documented pretrained agents
  - documented local agent-vs-agent and agent-vs-bot modes
  - supports data generation and replay-backed supervision
- Main risks:
  - older SC2 version assumptions
  - heavy stack
  - likely GPU-sensitive runtime
  - current public materials emphasize ZvZ and specific version constraints

### A2. `sc2egset_esports_dataset`

- Role:
  - preferred teacher-data source
- Source:
  - SC2EGSet article and Zenodo dataset
- License:
  - treat Zenodo record as authoritative: CC BY-NC 4.0
- Why it ranks second:
  - strong public teacher-data volume
  - tournament-derived data
  - useful for hidden-state and macro-outcome tasks
- Main risks:
  - not an online substrate
  - noncommercial terms
  - macro-action labels require derivation
  - mirror metadata conflict means the project should pin the Zenodo record, not
    a mirror, during acquisition

### B1. `ai_arena_downloadable_house_bots_pool`

- Role:
  - discovery pool for substrate/comparator/teacher
- Source:
  - AI Arena wiki plus downloadable bot ecosystem
- License:
  - unresolved per bot
- Why it still matters:
  - closest path to external-style bot ecosystem
  - local-play-bootstrap provides a ladder-compatible local environment family
  - downloadable bots and replay feeds could be valuable later
- Why it is not selected yet:
  - no per-bot license audit
  - intervention feasibility differs by bot
  - cannot treat downloaded performance as our contribution

### B2. `tstarbot_x_open_source_study`

- Role:
  - discovery candidate for substrate/teacher/comparator
- Source:
  - TStarBot-X paper
- License:
  - unresolved from current repo-first evidence
- Why it is interesting:
  - paper claims open code, resources, and trained parameters
  - strong full-game positioning
- Why it is not selected yet:
  - direct repository and license path were not yet audited in this task

## Preferred Path After Repair Audit

1. replacement online substrate target:
   - `sludge_revived_current_patch_house_bot`
2. retained teacher-source target:
   - `distar_zvz_agent_platform`
3. first teacher-data expansion target:
   - `sc2egset_esports_dataset`
4. external comparator pool to audit later:
   - `ai_arena_downloadable_house_bots_pool`

## Decision

The original candidate ranking was sufficient to enter acquisition, but it was
not sufficient to guarantee a viable current-patch online substrate.

After the failed DI-star online carrier repair path, substrate-only reranking is
now explicit:

The project has:

1. one preferred replacement substrate candidate with auditable license and
   current-patch claims:
   - `sludge_revived_current_patch_house_bot`
2. one retained teacher-first source that stays useful even if it is not the
   selected online substrate:
   - `distar_zvz_agent_platform`
3. at least one distinct teacher-data candidate:
   - `sc2egset_esports_dataset`
4. additional ecosystem candidates that remain discovery-only until deeper audit

## Source Notes

- AI Arena bot-development wiki states that:
  - local-play-bootstrap can run bot-vs-bot matches locally
  - downloadable bots and house bots exist
  - result replays can be downloaded
- `aiarena/sludge-revived` states that:
  - the repo is maintained for housebot usage on the AI Arena ladder
  - the bot supports Python 3.11 and SC2 patch 5.0.13
  - the original bot was estimated around high diamond or low masters level
- DI-star GitHub states that:
  - the repo includes playable demo and test code
  - pretrained SL and RL agents are provided
  - training code and replay/data materials are included
  - the project license is Apache-2.0
- SC2EGSet public records state that:
  - the dataset contains 55 replaypacks with 17930 game-state files
  - a Zenodo dataset record exists
  - the Zenodo record marks the dataset as CC BY-NC 4.0
- TStarBot-X paper states that:
  - code, resources, and trained parameters are publicly accessible
  - direct repository and license audit still remain to be done before selection
