# Phase A Baseline Real-Match Dataset V0 Sampling Plan

Status: planned.

This is a static sampling plan for Phase A2. It does not run SC2 and does not implement the reusable collection command.

## Goal

Collect a run-id scoped baseline real-match dataset large enough to support later Phase B/C/D iteration.

Target size:

- minimum closeout target: 24 real match attempts;
- preferred target: 24-48 real match attempts;
- chunk size: 8 matches per task by default.

## Run Scope

Canonical dataset run id:

- `phase_a_baseline_v0`

Historical run policy:

- do not mix historical runs into the current dataset by default;
- every chunk must use a scoped run id;
- merged manifest must explicitly list included chunk runs;
- merged manifest must explicitly list excluded historical runs when present.

## Coverage

Maps:

- `incorporeal_aie_v4`
- `leylines_aie_v3`

Opponents:

- `builtin_easy_terran`
- `builtin_medium_terran`
- `builtin_easy_zerg`
- `builtin_medium_zerg`
- `builtin_easy_protoss`
- `builtin_medium_protoss`

Bot config:

- `configs/bot/debug.yaml`

This keeps Phase A focused on data collection infrastructure. It does not claim gameplay strength.

## Chunk Plan

### Chunk 1

Run id:

- `phase_a_baseline_v0_chunk_1`

Matches:

- IncorporealAIE_v4 vs Terran Easy, repeats 2
- IncorporealAIE_v4 vs Terran Medium, repeats 2
- IncorporealAIE_v4 vs Zerg Easy, repeats 2
- IncorporealAIE_v4 vs Zerg Medium, repeats 2

Total: 8 matches.

### Chunk 2

Run id:

- `phase_a_baseline_v0_chunk_2`

Matches:

- IncorporealAIE_v4 vs Protoss Easy, repeats 2
- IncorporealAIE_v4 vs Protoss Medium, repeats 2
- LeyLinesAIE_v3 vs Terran Easy, repeats 2
- LeyLinesAIE_v3 vs Terran Medium, repeats 2

Total: 8 matches.

### Chunk 3

Run id:

- `phase_a_baseline_v0_chunk_3`

Matches:

- LeyLinesAIE_v3 vs Zerg Easy, repeats 2
- LeyLinesAIE_v3 vs Zerg Medium, repeats 2
- LeyLinesAIE_v3 vs Protoss Easy, repeats 2
- LeyLinesAIE_v3 vs Protoss Medium, repeats 2

Total: 8 matches.

## Closeout Threshold

Phase A2 baseline dataset V0 should reach at least 24 real match attempts before Phase A closeout.

If fewer than 24 matches are available, closeout must explicitly document:

- attempted match count;
- missing coverage;
- failure reason;
- whether the shortfall is accepted temporarily.

## Evidence Rules

- Chunk tasks must record evidence paths for every match directory.
- Merge task must produce `dataset_manifest.json`.
- Quality report must state that this dataset does not prove bot strength.
- Smoke output from A1 must not be merged into the baseline dataset unless a later task explicitly records it as historical or excluded evidence.
