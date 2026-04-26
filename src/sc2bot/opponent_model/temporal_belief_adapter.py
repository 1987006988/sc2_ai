"""Adapter from temporal-belief model outputs to stable prediction schema."""

from __future__ import annotations

from typing import Any

import torch

from sc2bot.opponent_model.interface import OpponentPrediction


OPENING_LABELS = ("econ_opening", "production_opening", "gas_opening")
TECH_LABELS = ("unknown", "gas_tech", "terran_bio_tech", "protoss_core_tech", "zerg_roach")
ARMY_LABELS = ("none", "low", "medium", "high")
THREAT_LABELS = ("standard_pressure", "immediate_pressure", "tech_transition")


def _argmax_label(logits: torch.Tensor, labels: tuple[str, ...]) -> str:
    return labels[int(torch.argmax(logits).item())]


def adapt_logits_to_prediction(outputs: dict[str, torch.Tensor]) -> OpponentPrediction:
    opening = _argmax_label(outputs["opening_class"], OPENING_LABELS)
    tech = _argmax_label(outputs["hidden_tech_path"], TECH_LABELS)
    army = _argmax_label(outputs["hidden_army_bucket"], ARMY_LABELS)
    threat = _argmax_label(outputs["next_macro_threat_indicator"], THREAT_LABELS)
    rush_prob = torch.sigmoid(outputs["future_contact_risk"]).item()
    tech_prob = 0.7 if tech != "unknown" else 0.2
    confidence = max(rush_prob, tech_prob)
    signals: list[str] = ["learned_temporal_belief"]
    if threat == "immediate_pressure":
        signals.append("future_contact_risk_high")
    if tech != "unknown":
        signals.append("hidden_tech_detected")
    recommended: list[str] = []
    if rush_prob >= 0.5:
        recommended.append("watch_for_rush")
    if tech_prob >= 0.5:
        recommended.append("watch_for_tech")
    return OpponentPrediction(
        model_name="temporal_gru_v0",
        opening_type=opening,
        rush_risk=round(float(rush_prob), 3),
        tech_risk=round(float(tech_prob), 3),
        enemy_army_estimate=army,
        confidence=round(float(confidence), 3),
        prediction_mode="learned_temporal_belief",
        signals=tuple(signals),
        recommended_response_tags=tuple(recommended),
    )


def adapt_batch_predictions(batch_outputs: dict[str, torch.Tensor]) -> list[OpponentPrediction]:
    batch_size = next(iter(batch_outputs.values())).shape[0]
    predictions: list[OpponentPrediction] = []
    for idx in range(batch_size):
        sample_outputs = {name: tensor[idx] for name, tensor in batch_outputs.items()}
        predictions.append(adapt_logits_to_prediction(sample_outputs))
    return predictions
