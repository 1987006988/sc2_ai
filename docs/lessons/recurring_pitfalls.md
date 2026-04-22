# Recurring Pitfalls

## Mainline contamination

Rule: Do not move prototype or notebook code into `src/sc2bot/` without promotion.

## Chat-only memory

Rule: Durable decisions must be written to `docs/adr/`, `docs/context/`, `docs/plans/`, or `docs/handoffs/`.

## Observation stream without scouting

Rule: A bot that only survives at home may produce valid telemetry but empty opponent observations. Keep at least one minimal scout path active before treating opponent-model input telemetry as validated.

## YAML reserved identifiers

Rule: Quote config IDs such as `"null"` in YAML. Unquoted `null` is parsed as `None`, which breaks ablation grouping and report labels.
