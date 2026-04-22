# Scope and Non-goals

## In Scope

- Layered hybrid full-game bot skeleton.
- Ares-sc2 / python-sc2 technical validation.
- AI Arena or equivalent local evaluation loop.
- Minimal telemetry and match logging.
- Opponent model interface and rule-based baseline.
- Research prototypes isolated under `research/`.

## Non-goals for Phase 1

- AlphaStar-like end-to-end RL.
- LLM real-time control.
- Full world model.
- SMAC as the full-game mainline.
- Production-grade replay imitation policy.
- Multi-race competitive bot.

## Boundary Rule

Research, validation, prototypes, and benchmark experiments must not be mixed into the production bot mainline.
