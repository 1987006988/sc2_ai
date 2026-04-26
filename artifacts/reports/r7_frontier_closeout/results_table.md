# R7 One-Page Results Table

| Layer | Setting | Comparator | Treatment | Outcome | Primary Evidence Path | Claim Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Offline | teacher benchmark holdout | rule_based `0.563704` | scratch_ensemble_v0 `0.569259` | learned beats strongest non-learning floor | `artifacts/models/r7_world_model/scratch_ensemble_v0.json` | accepted | single-source, proxy supervision |
| Internal | strong substrate vs builtin Medium Terran Timing | Arm A `Tie`, Arm B `Tie` | Arm C `Victory` | positive internal slice | `data/logs/evaluation/r7_online_intervention/r7_online_repair1_20260427/summary.json` | accepted | substrate = `sludge-revived` |
| External | strong substrate vs external `worker_rush` example bot | Arm A `Victory` | Arm C `Victory` | non-inferior external support | `data/logs/evaluation/r7_external_validation/r7_external_worker_rush_repair1/summary.json` | accepted | bounded downloaded-bot example slice |
