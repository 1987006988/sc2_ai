# R7 World Model Card

Model family: scratch action-conditioned macro world model
Updated: 2026-04-27

## Primary Variant

- variant:
  - `scratch_ensemble_v0`
- training source:
  - `data/r7/teacher_dataset/*.jsonl`
- output family:
  - hidden-state proxy heads
  - macro-action heads
  - future-outcome proxy heads
- action conditioning:
  - enabled in the selected future arm

## Selected Composition

The accepted offline model is a scratch-only selected ensemble:

1. `scratch_no_action_ruleaug` for hidden-state and macro-action groups
2. `scratch_full_ruleaug` for future-proxy groups

Holdout aggregate balanced accuracy:

- `0.569259`

Reference comparator floor:

- teacher-benchmark `rule_based = 0.563704`

## Claim Boundary

This model is trained on the current teacher-proxy dataset.

It is suitable for:

1. offline hidden-state proxy prediction
2. macro-action label prediction
3. future-outcome proxy prediction
4. later bounded advisor prototyping

It is not yet:

1. a validated online advisor
2. a fully grounded counterfactual simulator
3. a multi-source robust world model
4. a warm-start or externally pretrained model result
