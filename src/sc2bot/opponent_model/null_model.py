"""No-op opponent model used as the default safe baseline."""

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.interface import OpponentPrediction


class NullOpponentModel:
    model_name = "null"

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        _ = (observation, state)
        return OpponentPrediction(model_name=self.model_name)
