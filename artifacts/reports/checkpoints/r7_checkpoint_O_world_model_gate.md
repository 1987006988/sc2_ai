# R7 Checkpoint O: World Model Gate

Date: 2026-04-27

## Reviewed Tasks

- `r7_task_010_train_counterfactual_macro_world_model`
- `r7_task_011_compare_scratch_warmstart_and_external_baselines`

## Evidence Paths

- `configs/research/r7_train_world_model.yaml`
- `research/r7_world_model/train/train_world_model.py`
- `research/r7_world_model/models/action_conditioned_world_model.py`
- `research/r7_world_model/datasets/torch_dataset.py`
- `research/r7_world_model/eval/world_model_metrics.py`
- `research/r7_world_model/eval/results/r7_teacher_benchmark_v0.json`
- `artifacts/models/r7_world_model/scratch_full.json`
- `artifacts/models/r7_world_model/scratch_no_action.json`
- `artifacts/models/r7_world_model/scratch_full_ruleaug.json`
- `artifacts/models/r7_world_model/scratch_no_action_ruleaug.json`
- `artifacts/models/r7_world_model/scratch_ensemble_v0.json`
- `research/r7_world_model/cards/model_card.md`
- `artifacts/reports/r7_world_model_training/report.md`
- `artifacts/reports/r7_world_model_ablation/report.md`
- `artifacts/reports/checkpoints/r7_checkpoint_O_world_model_gate.md`

## Gate Result

- `minimum_gate_passed = true`
- `target_gate_passed = true`
- `stretch_gate_status = failed`
- `failure_class = none`
- `decision = accepted_continue`
- `next_allowed_task = r7_task_013_integrate_world_model_macro_advisor`

## Why It Passes

1. a scratch-trained R7 world-model family was trained end-to-end on the
   accepted teacher dataset
2. the accepted scratch-only ensemble beats the strongest non-learning holdout
   comparator on aggregate balanced accuracy:
   - `scratch_ensemble_v0 = 0.569259`
   - `rule_based = 0.563704`
3. the accepted result covers hidden-state, macro-action, and future-proxy
   output groups
4. the accepted claim is provenance-clean: no warm-start and no external
   pretrained world model are part of the accepted result

## Why Stretch Fails

1. no multi-architecture robustness result was established
2. no audited warm-start or external pretrained comparator was run
3. the accepted result still relies on teacher-proxy supervision and a
   single-source dataset
4. calibration is acceptable but not strong enough for a stretch-level claim

## Claim Boundary

This checkpoint accepts:

1. a scratch-first offline world-model result
2. provenance-safe comparator separation
3. entry into online advisor integration planning

This checkpoint does not accept:

1. online intervention value
2. external bot validation
3. richer counterfactual supervision beyond the current proxy labels
4. strong robustness across sources or architectures

## Invalid Evidence Excluded

1. no downloaded strong-bot raw performance is treated as our contribution
2. no warm-start or external pretrained model is hidden inside the accepted
   result
3. no online or external run is mixed into this offline checkpoint
4. no cherry-picked single-member scratch model is reported as the accepted
   result when the accepted artifact is the explicit scratch-only ensemble
