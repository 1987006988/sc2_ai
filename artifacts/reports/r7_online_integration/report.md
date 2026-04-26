# R7 Online Integration Report

Date: 2026-04-27
Status: completed
Phase: `phase_r7_4_online_intervention`

## Executed Tasks

- `r7_task_013_integrate_world_model_macro_advisor`
- `r7_task_014_run_online_strong_substrate_ablation`

## Accepted Substrate

- substrate:
  - `sludge_revived_current_patch_house_bot`
- source:
  - `https://github.com/aiarena/sludge-revived`
- acquired path:
  - `third_party/strong_bots/sludge-revived`
- commit:
  - `9703a799456751d6bba1fdbaf0c799636dddb7af`

Accepted roles now split cleanly:

1. `DI-star` remains the accepted `teacher`
2. `sludge-revived` is the accepted online `substrate`

## What Was Integrated

Implemented on the accepted substrate:

1. a substrate-local A/B/C wrapper:
   - `third_party/strong_bots/sludge-revived/bot/r7/bots.py`
2. a bounded rule advisor arm:
   - `third_party/strong_bots/sludge-revived/bot/r7/spending.py`
   - `third_party/strong_bots/sludge-revived/bot/r7/macro_advisor.py`
3. a substrate-local pure-Python world-model runtime:
   - `third_party/strong_bots/sludge-revived/bot/r7/macro_advisor.py`
   - runtime export:
     - `artifacts/models/r7_world_model/scratch_ensemble_v0_runtime.json`
4. an auditable single-match runner:
   - `third_party/strong_bots/sludge-revived/r7_run_eval.py`
5. one substrate compatibility repair:
   - `third_party/strong_bots/sludge-revived/sc2/paths.py`
   - purpose: choose the newest installed SC2 `BaseXXXXX` directory that actually contains `SC2_x64.exe`

## Replacement Runtime Validation

Validated Windows runtime:

- python:
  - `E:\dev\python\python3.11.5\python.exe`
- SC2 executable actually used:
  - `D:\games\StarCraft II\Versions\Base95841\SC2_x64.exe`

Verified:

1. baseline, rule, and world arms all import and launch on the same substrate
2. replay, result, and telemetry all save successfully
3. no historical Protoss carrier is used in the accepted evidence

## Accepted Online Slice

Accepted internal online run:

- run config manifest:
  - `configs/evaluation/r7_online_internal.yaml`
- accepted summary:
  - `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/summary.json`

Run contract:

- map:
  - `KairosJunctionLE`
- opponent:
  - `builtin Medium Terran Timing`
- game time limit:
  - `420`
- step time limit:
  - `2.0`

Arm definitions:

1. Arm A:
   - raw strong substrate
   - `baseline`
2. Arm B:
   - strong substrate + rule macro advisor
   - `rule`
3. Arm C:
   - strong substrate + learned world-model advisor
   - `world`

## Accepted Outcome Table

- Arm A baseline:
  - `Result.Tie`
- Arm B rule advisor:
  - `Result.Tie`
- Arm C learned world model:
  - `Result.Victory`

## Behavior Delta Summary

Arm A:

- no advisor applied
- terminal mode:
  - `attack`

Arm B:

- `advisor/applied_count = 1159`
- `defensive_hold = 1159`
- terminal mode:
  - `defend`

Arm C:

- `advisor/applied_count = 1135`
- action mix:
  - `add_tech = 475`
  - `defensive_hold = 133`
  - `increase_production_tempo = 527`
- priority injections after repair:
  - `army = 527`
  - `hatchery = 36`
- terminal mode:
  - `attack`

## Repair That Unblocked The Online Slice

Initial learned substrate behavior was real but mis-mapped:

1. `increase_production_tempo` over-produced Hatcheries on Zerg
2. `add_tech` triggered too early
3. the result was over-expansion and weak army conversion

Applied repair:

- file:
  - `third_party/strong_bots/sludge-revived/bot/r7/spending.py`

New bounded mapping:

1. tempo now prioritizes army first
2. Hatchery injection only occurs when worker, townhall, and army floors are met
3. Lair and Hydralisk Den only trigger after explicit econ and army thresholds

After that repair, the learned arm converted the same slice from tie-level play to
an actual `Victory`.

## Verification

Static:

```bash
python -m py_compile third_party/strong_bots/sludge-revived/r7_run_eval.py third_party/strong_bots/sludge-revived/bot/r7/*.py third_party/strong_bots/sludge-revived/bot/logic/unit_manager/unit_manager_v3.py
```

Windows import smoke:

```powershell
E:\dev\python\python3.11.5\python.exe -c "import sys; sys.path.insert(0, r'E:\software-work\strong_bots\sludge-revived'); import bot.r7.bots, bot.r7.spending, bot.r7.macro_advisor; print('R7_IMPORT_OK')"
```

Accepted run:

```powershell
E:\dev\python\python3.11.5\python.exe E:\software-work\strong_bots\sludge-revived\r7_run_eval.py --arm baseline|rule|world --map KairosJunctionLE --opponent-race Terran --difficulty Medium --ai-build Timing --game-time-limit 420 --step-time-limit 2.0 --output-dir ...
```

Observed:

1. all three arms launched
2. all three arms saved replay, result, and telemetry
3. no residual `SC2_x64` or evaluation python process remained after the accepted run

## Gate Judgement

### `r7_task_013`

- minimum gate:
  - `passed`
- target gate:
  - `passed`
- stretch gate:
  - `failed`

Reason:

1. the learned advisor now affects real macro decisions on the accepted strong substrate
2. A/B/C are arm-separated and auditable on the same substrate
3. the accepted online carrier is now truly strong-substrate-anchored
4. full macro-slate coverage is still incomplete

### `r7_task_014`

- minimum gate:
  - `passed`
- target gate:
  - `passed`
- stretch gate:
  - `failed`

Reason:

1. Arm C shows repeated behavior difference relative to A and B
2. Arm C converts the accepted slice to `Victory` while A and B remain `Tie`
3. the behavior delta is causal and localized to the bounded world-model advisor
4. accepted evidence is still a single internal slice, not broader robustness

## What This Proves

1. the R7 online path is now truly anchored on a stronger downloaded substrate
2. the learned world-model advisor can change macro behavior on that substrate
3. the learned arm can outperform both the raw substrate and the rule-advisor arm on an accepted internal slice

## What This Does Not Prove

1. it does not prove broader multi-map or multi-opponent online robustness
2. it does not prove external bot-ecosystem support
3. it does not prove the downloaded substrate's original strength is our contribution

## Invalid Evidence Excluded

1. the historical executable Protoss carrier runs remain diagnostic only:
   - `data/logs/evaluation/r7_online_probe/...`
   - `data/logs/evaluation/r7_online_intervention/r7_online_internal_20260427/summary.json`
2. the early DI-star online carrier attempt remains excluded from accepted online evidence
3. the pre-repair world-advisor over-expansion probe remains diagnostic context only
