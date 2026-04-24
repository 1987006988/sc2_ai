# task_007_rewrite_combat_unit_production_and_rally_logic

Date: 2026-04-24

## Scope

L1 implementation/static validation only.

## Changes

- narrowed `combat_unit_production_success` semantics to command-level evidence
  only; it now carries `evidence_semantics = command_only_not_unit_existence`
- runtime now records queue-entry evidence around train commands:
  - `pending_before_train`
  - `pending_after_train`
  - `pending_after_train_delta`
  - `queued_after_train`
- runtime now records gateway-side trainability context:
  - `available_gateway_abilities`
  - `active_alerts`
  - `units_created_total_for_unit`
- runtime now emits distinct army-presence lifecycle events:
  - `unit_created_detected`
  - `unit_alive_after_short_window`
  - `army_presence_changed`
- `unit_created_detected` now comes from `on_unit_created(...)` callback rather
  than step-level inference
- `army_presence_changed` now means observed `BotAI.army` count growth, not
  command issuance
- army-presence payloads now record:
  - `legacy_own_army_count`
  - `documented_own_army_count`
  - `combat_unit_count`
  - `observed_unit_tag`
  - `observed_unit_type`
  - `observation_source = bot_ai.army`
- pure helper logic was added so the production/army-presence contract can be
  unit-tested without running SC2
- tactical no-army guardrails remain in place: no rally/attack capability claim
  when `own_army_count = 0`

## Verification

Command:

- `PYTHONPATH=src:. python -m pytest tests/unit/test_game_loop.py tests/unit/test_tactical_manager.py tests/unit/test_build_progression_contract.py tests/integration/test_evaluation_config.py -q`

Result:

- `50 passed in 0.14s`

## What This Proves

- army-core prerequisites are now better structured for a real probe
- the runtime now distinguishes:
  - train command issued
  - queue entry observed after train
  - first observed unit creation
  - short-window survival
  - army-count growth
- `own_army_count` is now surrounded by dual-channel observation context
  (`legacy` vs `documented`) instead of standing alone
- no-army states are no longer mislabeled as rally/attack capability
- the next rerun can now separate:
  - queue-entry failure
  - materialization failure
  - state extraction / army classification failure

## What This Does Not Prove

- no real friendly army has been validated here
- no `own_army_count > 0` capability conclusion has been made here
- this does not by itself prove which one the next rerun will show:
  - `queue_entry_failure`
  - `true_materialization_failure`
  - `state_extraction_or_army_classification_failure`
