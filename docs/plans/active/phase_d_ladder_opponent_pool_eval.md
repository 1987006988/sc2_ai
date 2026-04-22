# Phase D: Ladder Opponent Pool Evaluation

Status: planned.

## Goal

Evaluate the bot against a broader ladder-like opponent pool and produce an opponent matrix that reflects real match capability.

## Scope

- built-in Easy / Medium / Hard opponents where feasible;
- scripted archetype opponents;
- AI Arena local, downloadable, or house bots where available;
- repeated matches;
- ladder evaluation report.

## Non-goals

- No new strategy features inside evaluation orchestration.
- No unsupported public-ladder claims.
- No manual cherry-picking of favorable replays as primary evidence.

## Files Likely To Change

- `configs/opponents/`
- `configs/evaluation/`
- `evaluation/runner/`
- `evaluation/metrics/`
- `evaluation/reports/`
- `docs/commands/`

## Verification

- Real repeated matches across the selected opponent pool.
- Report crash/timeout/win-rate/gameplay metrics.
- Store evidence paths for every match directory.
- Separate failed launches from gameplay losses.

## Done Criteria

- Opponent pool evaluation matrix exists.
- The matrix includes status, win/loss, crash/timeout, game duration, build completion, first scout, first attack, combat count, units killed/lost if available, defense response count, and strategy adaptation count.
- The report explicitly states pool limitations and evidence source.

## Stop Conditions

- If opponent setup is unreliable, stop and shrink to a stable subset.
- If external bot acquisition is blocked, proceed with built-in/scripted pool and document the gap.
- If repeated matches exceed runtime budget, split by pool segment.
