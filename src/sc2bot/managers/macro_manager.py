"""Macro manager skeleton."""

from sc2bot.domain.decisions import StrategyDecision
from sc2bot.domain.game_state import GameState


class MacroManager:
    """Handles economy, production, tech, and build-order execution."""

    def update(self, state: GameState, decision: StrategyDecision) -> None:
        _ = (state, decision)
