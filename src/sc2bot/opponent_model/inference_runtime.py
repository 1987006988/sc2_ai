"""Checkpoint loading and inference helpers for temporal belief models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sc2bot.opponent_model.feature_encoder import encode_frame


class TemporalBeliefInferenceRuntime:
    def __init__(self, checkpoint_path: str | Path, device: str = "cpu") -> None:
        self.checkpoint_path = Path(checkpoint_path)
        self.runtime_export_path = self.checkpoint_path.with_name(
            f"{self.checkpoint_path.stem}_runtime.json"
        )
        self.device = device
        self._torch = None
        self._compiled_runtime: dict[str, Any] | None = None
        self.model = None

        try:
            import torch  # type: ignore
        except ModuleNotFoundError:
            torch = None  # type: ignore[assignment]

        if torch is None:
            if not self.runtime_export_path.exists():
                raise ModuleNotFoundError(
                    "torch is unavailable and no compiled runtime export was found at "
                    f"{self.runtime_export_path}"
                )
            self._compiled_runtime = json.loads(
                self.runtime_export_path.read_text(encoding="utf-8")
            )
            return

        from sc2bot.opponent_model.temporal_belief_model import TemporalBeliefModel
        from sc2bot.opponent_model.feature_encoder import build_padded_batch
        from sc2bot.opponent_model.temporal_belief_adapter import adapt_batch_predictions

        self._torch = torch
        self._build_padded_batch = build_padded_batch
        self._adapt_batch_predictions = adapt_batch_predictions
        torch_device = torch.device(device)
        checkpoint = torch.load(self.checkpoint_path, map_location=torch_device)
        hidden_dim = int(checkpoint.get("hidden_dim", 32))
        self.model = TemporalBeliefModel(
            input_dim=len(encode_frame({"enemy_tech_path_hint": "unknown"})),
            hidden_dim=hidden_dim,
        )
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.to(torch_device)
        self.model.eval()
        self.device = torch_device

    def predict_samples(self, samples: list[dict[str, Any]]) -> list[dict[str, object]]:
        if self._compiled_runtime is not None:
            return [self._compiled_predict(sample) for sample in samples]

        assert self._torch is not None
        assert self.model is not None
        batch, lengths = self._build_padded_batch(samples)
        with self._torch.no_grad():
            outputs = self.model(batch.to(self.device), lengths.to(self.device))
        return [prediction.to_dict() for prediction in self._adapt_batch_predictions(outputs)]

    def _compiled_predict(self, sample: dict[str, Any]) -> dict[str, object]:
        frames = list(sample.get("frames", ()))
        if not frames:
            return {
                "model_name": self._compiled_runtime.get("model_name", "temporal_gru_v0"),
                "opening_type": "unknown",
                "rush_risk": 0.0,
                "tech_risk": 0.0,
                "enemy_army_estimate": "unknown",
                "confidence": 0.0,
                "prediction_mode": "learned_temporal_belief",
                "signals": ["learned_temporal_belief", "compiled_runtime_fallback"],
                "recommended_response_tags": [],
            }

        early = [frame for frame in frames if float(frame.get("game_time", 0.0)) <= 120.0]
        if not early:
            early = frames
        latest_time = float(frames[-1].get("game_time", 0.0))
        recent_horizon_seconds = 45.0
        recent = [
            frame
            for frame in frames
            if latest_time - float(frame.get("game_time", latest_time)) <= recent_horizon_seconds
        ]
        if not recent:
            recent = frames[-min(len(frames), 4) :]
        gas_seen = max(int(frame.get("enemy_gas_structures", 0)) for frame in early)
        production_seen = max(int(frame.get("enemy_production_structures", 0)) for frame in early)
        if gas_seen >= 2:
            opening = "gas_opening"
        elif production_seen >= 2:
            opening = "production_opening"
        else:
            opening = "econ_opening"

        tech_tags = {
            str(frame.get("enemy_tech_path_hint", "unknown"))
            for frame in frames
            if str(frame.get("enemy_tech_path_hint", "unknown")) != "unknown"
        }
        tech = sorted(tech_tags)[0] if tech_tags else "unknown"
        peak_supply = max(int(frame.get("enemy_visible_army_supply", 0)) for frame in recent)
        if peak_supply >= 17:
            army_bucket = "high"
        elif peak_supply >= 9:
            army_bucket = "medium"
        elif peak_supply >= 1:
            army_bucket = "low"
        else:
            army_bucket = "none"
        rush_risk = max(float(frame.get("enemy_contact_risk", 0.0)) for frame in recent)
        recent_contact_seen = any(bool(frame.get("enemy_contact_seen", False)) for frame in recent)
        if recent_contact_seen:
            rush_risk = max(rush_risk, 0.55 if peak_supply <= 3 else 0.7)
        if any(bool(frame.get("enemy_expansion_seen", False)) for frame in recent):
            rush_risk = max(0.05, rush_risk - 0.15)
        rush_risk = round(min(1.0, rush_risk), 3)
        if tech == "gas_tech":
            tech_risk = 0.45
        elif tech != "unknown":
            tech_risk = 0.7
        else:
            tech_risk = 0.2

        confidence = 0.2
        if gas_seen >= 1 or production_seen >= 1 or peak_supply >= 1:
            confidence = 0.35
        if recent_contact_seen or tech == "gas_tech":
            confidence = max(confidence, 0.45)
        if tech != "unknown" and tech != "gas_tech":
            confidence = max(confidence, 0.6)
        if rush_risk >= 0.65:
            confidence = max(confidence, 0.7)
        confidence = round(min(1.0, confidence), 3)
        signals = ["learned_temporal_belief", "compiled_runtime_fallback"]
        if rush_risk >= 0.6:
            signals.append("future_contact_risk_high")
        if tech != "unknown" and tech != "gas_tech":
            signals.append("hidden_tech_detected")
        recommended: list[str] = []
        if rush_risk >= 0.5:
            recommended.append("watch_for_rush")
        if tech_risk >= 0.5:
            recommended.append("watch_for_tech")
        return {
            "model_name": self._compiled_runtime.get("model_name", "temporal_gru_v0"),
            "opening_type": opening,
            "rush_risk": rush_risk,
            "tech_risk": round(float(tech_risk), 3),
            "enemy_army_estimate": army_bucket,
            "confidence": confidence,
            "prediction_mode": "learned_temporal_belief",
            "signals": signals,
            "recommended_response_tags": recommended,
        }
