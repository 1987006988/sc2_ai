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
- execution-layer army selection no longer depends on legacy `self.army` alone:
  - it still prefers legacy `self.army`
  - but it now falls back to documented combat-unit visibility from
    `self.units` for the currently supported combat-unit types
  - execution telemetry now records `execution_army_source`,
    `execution_army_count`, and `execution_idle_army_count`
- execution-layer target coercion now converts stored tuple positions into
  python-sc2 point targets before issuing `attack(...)` / `move(...)` commands
  on army units
- combat confirmation telemetry no longer depends only on pre-execution
  planning state:
  - runtime now records a post-execution combat-event assessment after command
    application or skip
  - post-execution payload carries execution outcome, execution reason, and
    applied command count
  - this lets later probes distinguish:
    - planning-only signals
    - execution applied with enemy contact
    - execution skipped for a concrete reason
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
42 passed in 0.06s
```

## What This Proves

- tactical order emission is now semantically cleaner and more auditable
- no-army / planning-only situations no longer look like friendly combat success
- runtime now exposes execution-layer command application telemetry separately
  from planning and combat inference
- execution-layer telemetry can now distinguish:
  - legacy army visible and executable
  - documented combat units visible only through `self.units`
  - genuinely no executable combat units
- execution-layer command application no longer sends raw tuple targets to
  python-sc2 army actions
- post-execution combat-event telemetry can now elevate execution-applied
  defend/attack signals above pure planning-only telemetry
- later real probes can review defend/attack telemetry without conflating plan signals with executed combat

## What This Does Not Prove

- no real SC2 tactical order has been validated in this task
- no friendly combat has been validated in this task
- this task does not prove target-level tactical stability
