# Phase L0: Ladder Readiness

Status: legacy_historical_reference
Execution authority: no
Superseded by: `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`

Legacy note: retained as historical phase planning context only. It must not be
used as the current execution authority.

## Goal

Make the bot usable in ladder-like bot-vs-bot evaluation and packaging flows.

This phase does not target strength. It targets entrypoint compatibility, repeated-match stability, persistence, and clear failure accounting.

## Scope

- AI Arena/local-play compatible entrypoint.
- Upload/package dry-run.
- Map and opponent configuration.
- Multi-match stability checks.
- Crash and timeout handling.
- Replay, match result, and telemetry persistence.
- Fixed evaluation command for repeated local runs.
- Crash rate and timeout rate summary.

## Non-goals

- No new complex build order.
- No gateway/gas/army production work beyond what later L1 defines.
- No strategy intervention expansion.
- No learning module integration.
- No win-rate claims.

## Files Likely To Change

- `evaluation/runner/`
- `configs/evaluation/`
- `configs/maps/`
- `configs/opponents/`
- `scripts/`
- `docs/commands/`
- package/upload metadata if already present in the project

## Verification

- Run a local ladder-like multi-match command.
- Confirm every match has isolated output.
- Confirm replay/result/telemetry persistence.
- Confirm crash and timeout are represented in structured output.
- Confirm package/upload dry-run checks expected files.

## Done Criteria

- A documented command can run multiple consecutive ladder-like matches.
- Match outputs include replay, match_result, telemetry, and structured status.
- Summary reports crash rate and timeout rate.
- Package structure can be checked without manual path edits.
- The phase does not claim competitive strength.

## Stop Conditions

- If entrypoint compatibility requires architecture changes, stop and write a design note.
- If real match launch becomes unstable, stop and isolate runtime failure before adding features.
- If packaging requirements are unclear, stop with a checklist rather than guessing.
