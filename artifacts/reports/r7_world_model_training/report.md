# R7 World Model Training Report

Date: 2026-04-27
Task: `r7_task_010_train_counterfactual_macro_world_model`

## Scope

This report covers scratch-first offline training of the first R7 learned world
model on the teacher-proxy dataset.

## Primary Variants

1. `scratch_full`
2. `scratch_no_action`
3. `scratch_full_ruleaug`
4. `scratch_no_action_ruleaug`
5. `scratch_ensemble_v0`

## Output Artifacts

- `artifacts/models/r7_world_model/scratch_full.pt`
- `artifacts/models/r7_world_model/scratch_full.json`
- `artifacts/models/r7_world_model/scratch_full_label_encoders.json`
- `artifacts/models/r7_world_model/scratch_no_action.pt`
- `artifacts/models/r7_world_model/scratch_no_action.json`
- `artifacts/models/r7_world_model/scratch_full_ruleaug.pt`
- `artifacts/models/r7_world_model/scratch_full_ruleaug.json`
- `artifacts/models/r7_world_model/scratch_no_action_ruleaug.pt`
- `artifacts/models/r7_world_model/scratch_no_action_ruleaug.json`
- `artifacts/models/r7_world_model/scratch_ensemble_v0.json`
- `research/r7_world_model/cards/model_card.md`

## Accepted Training Result

Selected offline primary result:

- `scratch_ensemble_v0`

Selection rule:

- use `scratch_no_action_ruleaug` for `hidden_state` and `macro_action` groups
- use `scratch_full_ruleaug` for `future_proxy` group

Test aggregate balanced accuracy:

- `scratch_ensemble_v0 = 0.569259`
- teacher benchmark `rule_based = 0.563704`
- teacher benchmark `static_prior = 0.416667`
- teacher benchmark `shallow_temporal = 0.337778`

Selected test group scores:

- `hidden_state = 0.805555`
- `macro_action = 0.402222`
- `future_proxy = 0.500000`

## Why Task 010 Passes

1. a scratch-only learned world-model family was trained on the accepted R7
   teacher dataset
2. checkpoints, result json files, and model metadata were saved
3. the selected scratch-only ensemble clears the teacher-benchmark aggregate
   baseline floor on the holdout split
4. no warm-start or external pretrained model is required for the accepted
   offline result

## Why Stretch Does Not Pass

1. no multi-architecture win was established
2. the accepted result still uses proxy supervision rather than richer
   counterfactual labels
3. calibration remains acceptable but not strong enough for a stretch claim
4. there is no multi-source robustness result yet

## Claim Boundary

This is a learned **proxy world-model result**.
It is allowed to support entry into online integration planning.
It is not an online gain claim.

It also remains:

1. scratch-only
2. offline-only
3. bounded to the current single-source DI-star-derived teacher dataset
