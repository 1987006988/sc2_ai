"""Feature encoding helpers for R6 temporal opponent-belief models."""

from __future__ import annotations

from typing import Any


TECH_HINT_INDEX = {
    "unknown": 0,
    "gas_tech": 1,
    "terran_bio_tech": 2,
    "protoss_core_tech": 3,
    "zerg_roach": 4,
}


def encode_frame(frame: dict[str, Any]) -> list[float]:
    tech_index = TECH_HINT_INDEX.get(str(frame.get("enemy_tech_path_hint", "unknown")), 0)
    one_hot = [0.0] * len(TECH_HINT_INDEX)
    one_hot[tech_index] = 1.0
    return [
        float(frame.get("game_time", 0.0)) / 300.0,
        float(frame.get("enemy_gas_structures", 0.0)) / 4.0,
        float(frame.get("enemy_production_structures", 0.0)) / 6.0,
        float(frame.get("enemy_visible_army_supply", 0.0)) / 20.0,
        float(frame.get("enemy_contact_risk", 0.0)),
        1.0 if bool(frame.get("enemy_contact_seen", False)) else 0.0,
        1.0 if bool(frame.get("enemy_expansion_seen", False)) else 0.0,
        *one_hot,
    ]


def encode_sample_frames(sample: dict[str, Any]) -> list[list[float]]:
    return [encode_frame(frame) for frame in sample.get("frames", [])]


def build_padded_batch(samples: list[dict[str, Any]]) -> tuple[torch.Tensor, torch.Tensor]:
    import torch

    sequences = [encode_sample_frames(sample) for sample in samples]
    lengths = torch.tensor([len(seq) for seq in sequences], dtype=torch.long)
    feature_dim = len(encode_frame({"enemy_tech_path_hint": "unknown"}))
    max_len = max((len(seq) for seq in sequences), default=1)
    batch = torch.zeros(len(samples), max_len, feature_dim, dtype=torch.float32)
    for row, sequence in enumerate(sequences):
        for col, frame in enumerate(sequence):
            batch[row, col] = torch.tensor(frame, dtype=torch.float32)
    return batch, lengths
