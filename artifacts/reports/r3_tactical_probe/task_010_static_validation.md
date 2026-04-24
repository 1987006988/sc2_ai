# task_010_rewrite_defend_attack_transition_logic

Date: 2026-04-25

## Scope

Static validation for tactical transition semantics only.

This task did not run real SC2 and did not validate friendly combat. It
rewrote tactical-plan and combat-event payload semantics so later probes can
distinguish:

- planning intent
- legal tactical prerequisites
- executed friendly-combat evidence

## Changes

- `TacticalPlan` now carries:
  - `defend_reason`
  - `attack_reason`
  - `regroup_reason`
  - `order_prerequisites_met`
  - `execution_evidence`
- runtime now records `tactical_order_execution` as a post-plan execution-layer
  event so later probes can distinguish:
  - plan emitted
  - command applied to army
  - contact/combat confirmed
- `TacticalManager.plan(...)` now:
  - keeps `defend_order` / `attack_order` gated on `own_army_count > 0`
  - records explicit attack/defend/regroup reasons
  - falls back to rally when attack thresholds are met but enemy start is still unknown
- `build_combat_event_payload(...)` is now conservative:
  - planning or visibility signals alone do not set `detected = true`
  - payload explicitly records planning vs prerequisite vs execution-evidence state

## Verification

Command:

```bash
PYTHONPATH=src:. python -m pytest tests/unit/test_tactical_manager.py tests/unit/test_telemetry_schema.py tests/unit/test_game_loop.py -q
```

Result:

```text
37 passed in 0.08s
```

## What This Proves

- tactical order emission is now semantically cleaner and more auditable
- no-army / planning-only situations no longer look like friendly combat success
- runtime now exposes execution-layer command application telemetry separately
  from planning and combat inference
- later real probes can review defend/attack telemetry without conflating plan signals with executed combat

## What This Does Not Prove

- no real SC2 tactical order has been validated in this task
- no friendly combat has been validated in this task
- this task does not prove target-level tactical stability
