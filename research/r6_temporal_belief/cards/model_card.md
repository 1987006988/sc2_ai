# R6 Temporal Belief Model Card

Model: `temporal_gru_v0`

Scope:

- first learned temporal belief model for R6 offline benchmark
- GRU encoder over compressed scouting-derived frame sequences
- first trained in Phase R6.2
- later integrated into bounded online response surface in Phase R6.3
- later validated on a narrow AI Arena-compatible local bot-vs-bot external slice in Phase R6.4

Training inputs:

- `research/r6_temporal_belief/data/materialized/train.jsonl`
- validation: `research/r6_temporal_belief/data/materialized/val.jsonl`
- holdout: `research/r6_temporal_belief/data/materialized/test.jsonl`

Primary task bundle:

- `opening_class`
- `hidden_tech_path`
- `hidden_army_bucket`
- `future_contact_risk`
- `next_macro_threat_indicator`

Non-claims:

- no broader external generalization claim
- no third-party downloadable house-bot generalization claim
- no multi-feature adaptive claim
