# R6 Ablation Table

## Offline Comparator Bundle

| Model | Aggregate holdout |
|---|---:|
| Static prior | `0.500` |
| Runtime-aligned rule-based | `0.825` |
| Learned temporal belief | `1.000` |

## Online / External Response Surface Comparison

| Arm | Opponent model mode | Intervention mode | External result vs comparator house bot |
|---|---|---|---|
| Frozen baseline | `rule_based` | `none` | `Tie` |
| Frozen R5 comparator | `rule_based` | `adaptive_gating` | `Victory` |
| Learned treatment | `learned_temporal_belief` | `adaptive_gating` | `Victory` |

## Interpretation

- the offline gain is not enough by itself
- the online internal gain is not enough by itself
- the accepted frontier closeout requires both of those plus the external slice
