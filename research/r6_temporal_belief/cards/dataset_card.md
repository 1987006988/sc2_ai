# R6 Temporal Belief Dataset Card

Dataset version: `r6_offline_benchmark_v0`

Primary manifests:

- `research/r6_temporal_belief/data/source_manifest.yaml`
- `research/r6_temporal_belief/data/dataset_manifest.json`
- `configs/research/r6_dataset_manifest.yaml`
- `configs/research/r6_label_schema.yaml`

Materialized splits:

- train: `research/r6_temporal_belief/data/materialized/train.jsonl`
- val: `research/r6_temporal_belief/data/materialized/val.jsonl`
- test: `research/r6_temporal_belief/data/materialized/test.jsonl`

Data sources:

- public replay corpora
- local historical replay corpora
- local accepted replay artifacts as domain anchors only

Usage boundaries:

- public and local historical corpora may support benchmark bootstrapping
- accepted R4/R5 artifacts are not used as holdout benchmark rows
- internal online evaluation replays do not flow back into the same accepted holdout benchmark

Primary tasks:

- `opening_class`
- `hidden_tech_path`
- `hidden_army_bucket`
- `future_contact_risk`
- `next_macro_threat_indicator`

Non-claims:

- no claim that this dataset is a public benchmark release
- no claim that the v0 task bundle is fully diverse
- no claim that accepted online or external replays are part of the accepted offline holdout
