from sc2bot.domain.observations import ScoutingObservation
from sc2bot.opponent_model.null_model import NullOpponentModel
from sc2bot.opponent_model.rule_based_model import RuleBasedOpponentModel


def test_null_opponent_model_returns_unknown_prediction():
    prediction = NullOpponentModel().predict(ScoutingObservation.empty())

    assert prediction.model_name == "null"
    assert prediction.opening_type == "unknown"
    assert prediction.prediction_mode == "prediction_only"
    assert prediction.to_dict()["signals"] == []


def test_rule_based_opponent_model_returns_confidence():
    prediction = RuleBasedOpponentModel().predict(
        ScoutingObservation(
            game_loop=100,
            enemy_units_seen=("zergling",),
            seen_enemy_combat_units=("zergling",),
        )
    )

    assert prediction.model_name == "rule_based"
    assert prediction.rush_risk > 0
    assert prediction.confidence >= 0
    assert "early_combat_unit" in prediction.signals


def test_rule_based_opponent_model_flags_tech_or_gas():
    prediction = RuleBasedOpponentModel().predict(
        ScoutingObservation(
            game_loop=900,
            game_time=40.0,
            enemy_structures_seen=("refinery", "barracks"),
            seen_enemy_structures=("refinery", "barracks"),
            observation_confidence=0.4,
        )
    )

    assert prediction.tech_risk >= 0.5
    assert "tech_or_gas" in prediction.signals
    assert prediction.prediction_mode == "prediction_only"


def test_rule_based_opponent_model_flags_production_structure():
    prediction = RuleBasedOpponentModel().predict(
        ScoutingObservation(
            game_loop=700,
            game_time=31.0,
            enemy_structures_seen=("gateway",),
            seen_enemy_structures=("gateway",),
            observation_confidence=0.3,
        )
    )

    assert prediction.opening_type == "production_seen"
    assert "production_structure" in prediction.signals
    assert "prediction_only" in prediction.recommended_response_tags


def test_rule_based_opponent_model_marks_low_information():
    prediction = RuleBasedOpponentModel().predict(
        ScoutingObservation(game_loop=2016, game_time=95.0)
    )

    assert "low_information" in prediction.signals
    assert prediction.confidence <= 0.2


def test_rule_based_opponent_model_reduces_rush_risk_for_expansion():
    prediction = RuleBasedOpponentModel().predict(
        ScoutingObservation(
            game_loop=1200,
            game_time=55.0,
            seen_enemy_combat_units=("zergling",),
            enemy_expansion_seen=True,
            observation_confidence=0.5,
        )
    )

    assert prediction.opening_type == "macro_or_expand"
    assert "expansion_seen" in prediction.signals
    assert prediction.rush_risk < 0.55
