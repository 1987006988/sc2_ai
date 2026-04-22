"""Micro manager skeleton."""

from sc2bot.domain.decisions import TacticalPlan
from sc2bot.domain.game_state import GameState


class MicroManager:
    """Executes low-level unit control.

    Phase 1 keeps this rule-based and minimal. SMAC policies do not live here
    unless promoted from research.
    """

    def execute(self, state: GameState, plan: TacticalPlan) -> None:
        _ = (state, plan)
