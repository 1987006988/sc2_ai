"""Minimal rule-based opponent model placeholder."""

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.interface import OpponentPrediction

_PRODUCTION_STRUCTURES = {
    "barracks",
    "gateway",
    "spawningpool",
    "spawning_pool",
}

_TECH_OR_GAS_STRUCTURES = {
    "assimilator",
    "barrackstechlab",
    "cyberneticscore",
    "extractor",
    "factory",
    "lair",
    "refinery",
    "roboticsfacility",
    "spire",
    "stargate",
    "starport",
    "twilightcouncil",
}


class RuleBasedOpponentModel:
    """Phase-1 baseline; real rules should be added behind tests and ablations."""

    model_name = "rule_based"

    def predict(
        self,
        observation: ScoutingObservation,
        state: GameState | None = None,
    ) -> OpponentPrediction:
        _ = state
        structures = {item.lower().replace("_", "") for item in observation.enemy_structures_seen}
        combat_units = set(observation.seen_enemy_combat_units)
        signals: list[str] = []
        rush_risk = 0.1
        tech_risk = 0.05
        opening_type = "unknown"

        if combat_units:
            rush_risk = 0.55
            signals.append("early_combat_unit")
            opening_type = "combat_units_seen"

        if structures.intersection({item.replace("_", "") for item in _PRODUCTION_STRUCTURES}):
            signals.append("production_structure")
            if opening_type == "unknown":
                opening_type = "production_seen"

        if structures.intersection({item.replace("_", "") for item in _TECH_OR_GAS_STRUCTURES}):
            tech_risk = 0.5
            signals.append("tech_or_gas")
            if opening_type in {"unknown", "production_seen"}:
                opening_type = "tech_or_gas_seen"

        if observation.enemy_expansion_seen:
            rush_risk = max(0.05, rush_risk - 0.2)
            signals.append("expansion_seen")
            opening_type = "macro_or_expand"

        if observation.first_enemy_seen_time is None and observation.game_time >= 90.0:
            signals.append("low_information")

        confidence = observation.observation_confidence
        if signals:
            confidence = max(confidence, 0.35)
        if "low_information" in signals:
            confidence = min(confidence, 0.2)

        response_tags: list[str] = ["prediction_only"]
        if rush_risk >= 0.5:
            response_tags.append("watch_for_rush")
        if tech_risk >= 0.5:
            response_tags.append("watch_for_tech")

        return OpponentPrediction(
            model_name=self.model_name,
            opening_type=opening_type,
            rush_risk=rush_risk,
            tech_risk=tech_risk,
            enemy_army_estimate="combat_seen" if combat_units else "unknown",
            confidence=round(min(1.0, confidence), 3),
            signals=tuple(signals),
            recommended_response_tags=tuple(response_tags),
        )
