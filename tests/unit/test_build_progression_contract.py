from sc2bot.domain.build_progression import (
    ARMY_RALLY,
    ASSIMILATOR,
    ATTACK_ORDER,
    COMBAT_EVENT,
    CYBERNETICS_CORE,
    DEFEND_ORDER,
    GATEWAY,
    PROBE_PRODUCTION,
    PYLON,
    REQUIRED_PHASE_B_FEATURES,
    STALKER,
    ZEALOT,
    BuildProgressionContract,
)


def test_phase_b_contract_contains_required_features():
    contract = BuildProgressionContract()

    assert contract.required_features == REQUIRED_PHASE_B_FEATURES
    assert set(contract.required_features) == {
        PROBE_PRODUCTION,
        PYLON,
        GATEWAY,
        ASSIMILATOR,
        CYBERNETICS_CORE,
        ZEALOT,
        STALKER,
        ARMY_RALLY,
        ATTACK_ORDER,
        DEFEND_ORDER,
        COMBAT_EVENT,
    }
    assert contract.validation_errors() == []


def test_phase_b_contract_groups_features_for_later_telemetry():
    contract = BuildProgressionContract()

    assert contract.build_features == (
        PROBE_PRODUCTION,
        PYLON,
        GATEWAY,
        ASSIMILATOR,
        CYBERNETICS_CORE,
    )
    assert contract.combat_unit_features == (ZEALOT, STALKER)
    assert contract.army_order_features == (ARMY_RALLY, ATTACK_ORDER, DEFEND_ORDER)
    assert contract.telemetry_features == (COMBAT_EVENT,)


def test_phase_b_contract_serializes_for_docs_and_reports():
    payload = BuildProgressionContract().to_dict()

    assert payload["required_features"] == list(REQUIRED_PHASE_B_FEATURES)
    assert payload["validation_level_required"] == "L3"
    assert "Real SC2 probes are required before gameplay behavior is validated." in payload["notes"]


def test_phase_b_contract_reports_missing_features():
    contract = BuildProgressionContract(
        build_features=(PROBE_PRODUCTION, PYLON),
        combat_unit_features=(),
        army_order_features=(),
        telemetry_features=(),
    )

    assert contract.missing_required_features() == (
        GATEWAY,
        ASSIMILATOR,
        CYBERNETICS_CORE,
        ZEALOT,
        STALKER,
        ARMY_RALLY,
        ATTACK_ORDER,
        DEFEND_ORDER,
        COMBAT_EVENT,
    )
    assert contract.validation_errors() == [
        "missing required features: gateway, assimilator, cybernetics_core, zealot, stalker, army_rally, attack_order, defend_order, combat_event"
    ]
