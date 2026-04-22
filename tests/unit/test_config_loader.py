from pathlib import Path

from sc2bot.config.loader import load_bot_config


def test_load_default_config():
    config = load_bot_config(Path("configs/bot/default.yaml"))

    assert config.bot.name == "sc2-ai-skeleton"
    assert config.opponent_model.mode == "null"
    assert config.opponent_model.intervention_mode == "none"
    assert config.opponent_model.rush_risk_threshold == 0.5
    assert config.opponent_model.tech_risk_threshold == 0.5
    assert config.opponent_model.low_information_confidence_threshold == 0.25
    assert config.opponent_model.low_information_game_time_threshold == 90.0
    assert config.runtime.max_game_loop == 2600
    assert config.runtime.worker_production is True
    assert config.runtime.worker_scout is True
    assert config.runtime.supply_sustain is True
    assert config.runtime.supply_sustain_threshold == 2
    assert config.build_order.target_probe_count == 22
    assert config.build_order.pylon_supply_buffer == 2
    assert config.build_order.gateway_min_probe_count == 16
    assert config.build_order.gateway_min_game_time == 90.0
    assert config.build_order.assimilator_enabled is True
    assert config.build_order.cybernetics_core_enabled is True
    assert config.build_order.zealot_production_priority == 10
    assert config.build_order.stalker_production_priority == 20
    assert config.build_order.attack_army_supply_threshold == 8
    assert config.build_order.attack_game_time_threshold == 360.0
    assert config.build_order.defend_radius == 30.0
    assert config.telemetry.enabled is True


def test_load_phase1d_opponent_model_configs():
    null_config = load_bot_config(Path("configs/bot/opponent_model_null.yaml"))
    rule_config = load_bot_config(Path("configs/bot/opponent_model_rule_based.yaml"))

    assert null_config.opponent_model.mode == "null"
    assert null_config.opponent_model.intervention_mode == "none"
    assert rule_config.opponent_model.mode == "rule_based"
    assert rule_config.opponent_model.intervention_mode == "none"
    assert null_config.runtime.supply_structure_name == "pylon"
    assert rule_config.runtime.supply_sustain is True


def test_load_phase1e_tag_only_config():
    config = load_bot_config(Path("configs/bot/opponent_model_tag_only.yaml"))

    assert config.opponent_model.mode == "rule_based"
    assert config.opponent_model.intervention_mode == "tag_only"
    assert config.opponent_model.rush_risk_threshold == 0.5
    assert config.opponent_model.tech_risk_threshold == 0.5
    assert config.opponent_model.low_information_confidence_threshold == 0.25
    assert config.opponent_model.low_information_game_time_threshold == 90.0
    assert config.runtime.supply_sustain is True


def test_build_order_config_defaults_keep_existing_configs_compatible():
    config = load_bot_config(Path("configs/bot/opponent_model_null.yaml"))

    assert config.build_order.target_probe_count == 22
    assert config.build_order.pylon_supply_buffer == 2
    assert config.build_order.gateway_min_probe_count == 16
    assert config.build_order.gateway_min_game_time == 90.0
    assert config.build_order.assimilator_enabled is True
    assert config.build_order.cybernetics_core_enabled is True
    assert config.build_order.zealot_production_priority == 10
    assert config.build_order.stalker_production_priority == 20
    assert config.build_order.attack_army_supply_threshold == 8
    assert config.build_order.attack_game_time_threshold == 360.0
    assert config.build_order.defend_radius == 30.0
