from __future__ import annotations

from pathlib import Path

import torch

from sc2bot.opponent_model.feature_encoder import build_padded_batch
from sc2bot.opponent_model.inference_runtime import TemporalBeliefInferenceRuntime
from sc2bot.opponent_model.temporal_belief_adapter import adapt_batch_predictions
from sc2bot.opponent_model.temporal_belief_model import TemporalBeliefModel


def _samples() -> list[dict]:
    return [
        {
            "replay_id": "sample-a",
            "replay_series_id": "series-a",
            "player_identity": "builtin_easy_zerg:default",
            "time_window_bucket": "2026-04-20",
            "latest_observation": {},
            "frames": [
                {"game_time": 0.0, "enemy_gas_structures": 0, "enemy_production_structures": 1, "enemy_visible_army_supply": 0, "enemy_contact_risk": 0.1, "enemy_contact_seen": False, "enemy_expansion_seen": False, "enemy_tech_path_hint": "unknown"},
                {"game_time": 55.0, "enemy_gas_structures": 2, "enemy_production_structures": 1, "enemy_visible_army_supply": 2, "enemy_contact_risk": 0.8, "enemy_contact_seen": True, "enemy_expansion_seen": False, "enemy_tech_path_hint": "gas_tech"},
            ],
        },
        {
            "replay_id": "sample-b",
            "replay_series_id": "series-b",
            "player_identity": "builtin_easy_terran:default",
            "time_window_bucket": "2026-04-21",
            "latest_observation": {},
            "frames": [
                {"game_time": 0.0, "enemy_gas_structures": 0, "enemy_production_structures": 1, "enemy_visible_army_supply": 0, "enemy_contact_risk": 0.1, "enemy_contact_seen": False, "enemy_expansion_seen": False, "enemy_tech_path_hint": "unknown"},
                {"game_time": 65.0, "enemy_gas_structures": 1, "enemy_production_structures": 2, "enemy_visible_army_supply": 1, "enemy_contact_risk": 0.45, "enemy_contact_seen": False, "enemy_expansion_seen": False, "enemy_tech_path_hint": "terran_bio_tech"},
            ],
        },
    ]


def test_temporal_model_outputs_schema_valid_prediction_batch(tmp_path: Path):
    samples = _samples()
    batch, lengths = build_padded_batch(samples)
    model = TemporalBeliefModel(input_dim=batch.shape[-1], hidden_dim=8)
    outputs = model(batch, lengths)
    predictions = adapt_batch_predictions(outputs)
    assert len(predictions) == 2
    payload = predictions[0].to_dict()
    assert payload["model_name"] == "temporal_gru_v0"
    assert payload["prediction_mode"] == "learned_temporal_belief"

    checkpoint_path = tmp_path / "model.pt"
    torch.save({"model_state_dict": model.state_dict(), "hidden_dim": 8}, checkpoint_path)
    runtime = TemporalBeliefInferenceRuntime(checkpoint_path)
    runtime_predictions = runtime.predict_samples(samples)
    assert len(runtime_predictions) == 2
    assert runtime_predictions[0]["model_name"] == "temporal_gru_v0"


def test_compiled_runtime_fallback_does_not_keep_stale_contact_risk_latched():
    runtime = TemporalBeliefInferenceRuntime.__new__(TemporalBeliefInferenceRuntime)
    runtime._compiled_runtime = {"model_name": "temporal_gru_v0"}

    prediction = runtime._compiled_predict(
        {
            "frames": [
                {
                    "game_time": 0.0,
                    "enemy_gas_structures": 0,
                    "enemy_production_structures": 1,
                    "enemy_visible_army_supply": 0,
                    "enemy_contact_risk": 0.1,
                    "enemy_contact_seen": False,
                    "enemy_expansion_seen": False,
                    "enemy_tech_path_hint": "unknown",
                },
                {
                    "game_time": 55.0,
                    "enemy_gas_structures": 0,
                    "enemy_production_structures": 1,
                    "enemy_visible_army_supply": 2,
                    "enemy_contact_risk": 0.8,
                    "enemy_contact_seen": True,
                    "enemy_expansion_seen": False,
                    "enemy_tech_path_hint": "unknown",
                },
                {
                    "game_time": 140.0,
                    "enemy_gas_structures": 0,
                    "enemy_production_structures": 1,
                    "enemy_visible_army_supply": 0,
                    "enemy_contact_risk": 0.1,
                    "enemy_contact_seen": False,
                    "enemy_expansion_seen": False,
                    "enemy_tech_path_hint": "unknown",
                },
            ]
        }
    )

    assert prediction["rush_risk"] == 0.1
    assert "watch_for_rush" not in prediction["recommended_response_tags"]


def test_compiled_runtime_fallback_treats_gas_tech_as_moderate_not_hard_tech_alert():
    runtime = TemporalBeliefInferenceRuntime.__new__(TemporalBeliefInferenceRuntime)
    runtime._compiled_runtime = {"model_name": "temporal_gru_v0"}

    prediction = runtime._compiled_predict(
        {
            "frames": [
                {
                    "game_time": 0.0,
                    "enemy_gas_structures": 2,
                    "enemy_production_structures": 1,
                    "enemy_visible_army_supply": 0,
                    "enemy_contact_risk": 0.1,
                    "enemy_contact_seen": False,
                    "enemy_expansion_seen": False,
                    "enemy_tech_path_hint": "gas_tech",
                }
            ]
        }
    )

    assert prediction["tech_risk"] == 0.45
    assert "watch_for_tech" not in prediction["recommended_response_tags"]
