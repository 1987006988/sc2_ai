"""Runtime wrapper for the R6 learned temporal belief checkpoint."""

from __future__ import annotations

from collections import deque
from typing import Any

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.inference_runtime import TemporalBeliefInferenceRuntime
from sc2bot.opponent_model.interface import OpponentPrediction

_GAS_STRUCTURE_HINTS = {"assimilator", "extractor", "refinery"}
_PRODUCTION_STRUCTURE_HINTS = {
    "barracks",
    "gateway",
    "spawningpool",
    "spawning_pool",
    "roboticsfacility",
    "stargate",
    "starport",
    "factory",
}


def _normalize(name: str) -> str:
    return str(name).lower().replace("_", "")


def _tech_hint(observation: ScoutingObservation) -> str:
    structures = {_normalize(name) for name in observation.seen_enemy_structures}
    if "barrackstechlab" in structures:
        return "terran_bio_tech"
    if "cyberneticscore" in structures:
        return "protoss_core_tech"
    if "roachwarren" in structures:
        return "zerg_roach"
    gas_count = sum(1 for name in structures if name in _GAS_STRUCTURE_HINTS)
    if gas_count >= 2 or observation.possible_tech_signal:
        return "gas_tech"
    return "unknown"


def observation_to_temporal_frame(observation: ScoutingObservation) -> dict[str, Any]:
    structures = [_normalize(name) for name in observation.current_enemy_structures]
    gas_count = sum(1 for name in structures if name in _GAS_STRUCTURE_HINTS)
    production_count = sum(1 for name in structures if name in _PRODUCTION_STRUCTURE_HINTS)
    visible_army_supply = len(observation.current_enemy_combat_units)
    early_contact = (
        visible_army_supply > 0
        and observation.first_enemy_seen_time is not None
        and observation.first_enemy_seen_time <= 180.0
    )
    if visible_army_supply <= 0:
        contact_risk = 0.1
    elif early_contact and visible_army_supply >= 4:
        contact_risk = 0.7
    else:
        contact_risk = 0.55 if early_contact else 0.45
    return {
        "game_time": observation.game_time,
        "enemy_gas_structures": gas_count,
        "enemy_production_structures": production_count,
        "enemy_visible_army_supply": visible_army_supply,
        "enemy_contact_risk": contact_risk,
        "enemy_contact_seen": bool(observation.current_enemy_combat_units),
        "enemy_expansion_seen": observation.enemy_expansion_seen,
        "enemy_tech_path_hint": _tech_hint(observation),
    }


class TemporalBeliefOpponentModel:
    """Inference-time temporal wrapper that maintains a bounded observation history."""

    model_name = "temporal_gru_v0"

    def __init__(
        self,
        checkpoint_path: str,
        *,
        device: str = "cpu",
        history_window: int = 8,
    ) -> None:
        self.runtime = TemporalBeliefInferenceRuntime(checkpoint_path, device=device)
        self.history_window = max(1, int(history_window))
        self._frames: deque[dict[str, Any]] = deque(maxlen=self.history_window)

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        _ = state
        self._frames.append(observation_to_temporal_frame(observation))
        payload = self.runtime.predict_samples(
            [
                {
                    "frames": list(self._frames),
                    "latest_observation": observation.to_dict(),
                }
            ]
        )[0]
        return OpponentPrediction(
            model_name=str(payload.get("model_name", self.model_name)),
            opening_type=str(payload.get("opening_type", "unknown")),
            rush_risk=float(payload.get("rush_risk", 0.0)),
            tech_risk=float(payload.get("tech_risk", 0.0)),
            enemy_army_estimate=str(payload.get("enemy_army_estimate", "unknown")),
            confidence=float(payload.get("confidence", 0.0)),
            prediction_mode=str(payload.get("prediction_mode", "learned_temporal_belief")),
            signals=tuple(payload.get("signals", [])),
            recommended_response_tags=tuple(payload.get("recommended_response_tags", [])),
        )
