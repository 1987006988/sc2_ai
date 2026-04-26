# R7 World Model Ablation Report

Date: 2026-04-27
Task: `r7_task_011_compare_scratch_warmstart_and_external_baselines`

## Scope

This report protects model provenance and compares the scratch primary model
against available internal ablations.

## Comparator Policy

Warm-start and external pretrained world-model baselines were not used in this
turn.

Reason:

1. no audited warm-start world-model source is selected inside R7 scope yet
2. the primary R7 claim should remain scratch-first if possible

## Compared Variants

1. `scratch_full`
2. `scratch_no_action`
3. `scratch_full_ruleaug`
4. `scratch_no_action_ruleaug`
5. `scratch_ensemble_v0`
6. non-learning teacher benchmark baselines

## Accepted Provenance Conclusion

The accepted phase-R7.3 result remains scratch-first.

Accepted artifact:

- `artifacts/models/r7_world_model/scratch_ensemble_v0.json`

Accepted provenance boundary:

1. no warm-start checkpoint was used
2. no external pretrained world model was used
3. the accepted result is an internal selection across scratch-trained members
4. the accepted claim is offline capability only

## Selected Comparison Summary

Holdout aggregate balanced accuracy on the teacher benchmark:

- `rule_based = 0.563704`
- `scratch_full = 0.479908`
- `scratch_no_action = 0.424352`
- `scratch_full_ruleaug = 0.456296`
- `scratch_no_action_ruleaug = 0.540092`
- `scratch_ensemble_v0 = 0.569259`

Interpretation:

1. single scratch members alone did not consistently beat the strongest
   non-learning comparator
2. scratch-only selection across specialized members did beat the aggregate
   rule-based floor
3. this is enough to preserve a scratch-first primary claim for checkpoint O
4. it is not enough to support a stretch claim about architecture robustness

## Why Task 011 Passes

1. scratch provenance is explicit
2. warm-start and external models remain outside the accepted claim
3. the accepted selected result is reproducible from saved scratch artifacts
4. the claim does not depend on downloaded-model performance

## Why Stretch Does Not Pass

1. no audited warm-start comparator was run
2. no external pretrained comparator was run
3. no multi-architecture robustness win was established beyond the selected
   scratch ensemble

## Claim Boundary

The primary claim remains scratch-first because the accepted result uses only
scratch-trained members and explicitly excludes warm-start or external
pretrained dependencies.
