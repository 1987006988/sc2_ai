from __future__ import annotations

import json
from pathlib import Path

from research.r6_temporal_belief.datasets.reader import load_and_validate_jsonl
from research.r6_temporal_belief.eval.metrics import evaluate_prediction_bundle
from research.r6_temporal_belief.eval.offline_baselines import (
    build_static_prior,
    label_dict,
    rule_based_predictor,
    shallow_temporal_predictor,
    static_prior_predictor,
)
from research.r6_temporal_belief.labels.labelers import extract_hidden_state_labels


def _samples() -> list[dict]:
    return [
        {
            "replay_id": "r1",
            "replay_series_id": "s1",
            "player_identity": "p1",
            "time_window_bucket": "t1",
            "frames": [
                {"game_time": 0, "enemy_gas_structures": 0, "enemy_production_structures": 1, "enemy_visible_army_supply": 2, "enemy_contact_risk": 0.2},
                {"game_time": 60, "enemy_gas_structures": 2, "enemy_production_structures": 1, "enemy_visible_army_supply": 6, "enemy_contact_risk": 0.4, "enemy_tech_path_hint": "stargate"},
                {"game_time": 120, "enemy_gas_structures": 2, "enemy_expansion_seen": True, "enemy_visible_army_supply": 10, "enemy_contact_risk": 0.8, "enemy_contact_seen": True, "enemy_tech_path_hint": "stargate"},
            ],
        },
        {
            "replay_id": "r2",
            "replay_series_id": "s2",
            "player_identity": "p2",
            "time_window_bucket": "t2",
            "frames": [
                {"game_time": 0, "enemy_gas_structures": 0, "enemy_production_structures": 2, "enemy_visible_army_supply": 4, "enemy_contact_risk": 0.1},
                {"game_time": 70, "enemy_gas_structures": 0, "enemy_production_structures": 2, "enemy_visible_army_supply": 13, "enemy_contact_risk": 0.3},
                {"game_time": 130, "enemy_gas_structures": 0, "enemy_visible_army_supply": 18, "enemy_contact_risk": 0.5},
            ],
        },
        {
            "replay_id": "r3",
            "replay_series_id": "s3",
            "player_identity": "p3",
            "time_window_bucket": "t3",
            "frames": [
                {"game_time": 0, "enemy_gas_structures": 1, "enemy_production_structures": 1, "enemy_visible_army_supply": 1, "enemy_contact_risk": 0.2},
                {"game_time": 75, "enemy_gas_structures": 1, "enemy_production_structures": 1, "enemy_visible_army_supply": 3, "enemy_contact_risk": 0.2},
                {"game_time": 150, "enemy_gas_structures": 1, "enemy_production_structures": 1, "enemy_visible_army_supply": 5, "enemy_contact_risk": 0.2},
            ],
        },
    ]


def test_extract_hidden_state_labels_covers_multiple_tasks():
    labels = extract_hidden_state_labels(_samples()[0])
    assert labels.opening_class == "gas_opening"
    assert labels.hidden_tech_path == "stargate"
    assert labels.future_expansion_within_horizon is True
    assert labels.hidden_army_bucket == "medium"
    assert labels.future_contact_risk is True
    assert labels.time_to_first_contact == 120.0


def test_dataset_reader_validates_jsonl_subset(tmp_path: Path):
    path = tmp_path / "subset.jsonl"
    path.write_text("\n".join(json.dumps(sample) for sample in _samples()), encoding="utf-8")
    samples, errors = load_and_validate_jsonl(path)
    assert len(samples) == 3
    assert errors == []


def test_baselines_run_end_to_end_on_fixture_subset():
    samples = _samples()
    truths = [label_dict(sample) for sample in samples]
    priors = build_static_prior(samples)

    rule_preds = [rule_based_predictor(sample) for sample in samples]
    prior_preds = [static_prior_predictor(priors, sample) for sample in samples]
    shallow_preds = [shallow_temporal_predictor(sample) for sample in samples]

    rule_report = evaluate_prediction_bundle(truths, rule_preds)
    prior_report = evaluate_prediction_bundle(truths, prior_preds)
    shallow_report = evaluate_prediction_bundle(truths, shallow_preds)

    assert "opening_class" in rule_report
    assert 0.0 <= rule_report["opening_class"]["accuracy"] <= 1.0
    assert "hidden_army_bucket" in prior_report
    assert 0.0 <= shallow_report["future_contact_risk"]["accuracy"] <= 1.0
