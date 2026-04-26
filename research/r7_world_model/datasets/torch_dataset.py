from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from torch import Tensor
from torch.utils.data import Dataset

from research.r7_world_model.datasets.reader import load_and_validate_jsonl


TASK_NAMES = (
    "enemy_opening_class",
    "enemy_tech_path",
    "macro_action_label",
    "production_tempo_label",
    "future_winner",
    "future_game_length_bucket",
    "future_pressure_proxy",
)
RACES = ("Protoss", "Terran", "Zerg", "Random")


def _one_hot(value: str, vocab: tuple[str, ...]) -> list[float]:
    return [1.0 if value == candidate else 0.0 for candidate in vocab]


def feature_vector(sample: dict[str, Any]) -> list[float]:
    own = sample["own_visible_state"]
    observed_enemy = sample["observed_enemy_state"]
    vector = [
        float(own["expand_count"]),
        float(own["production_count"]),
        float(own["tech_count"]),
        float(own["upgrade_count"]),
        float(own["defense_count"]),
        float(own["combat_unit_count"]),
        float(own["worker_econ_count"]),
        float(own["attack_count"]),
    ]
    for frame in sample["frames"]:
        vector.extend(
            [
                float(frame["expand_count"]),
                float(frame["production_count"]),
                float(frame["tech_count"]),
                float(frame["upgrade_count"]),
                float(frame["defense_count"]),
                float(frame["combat_unit_count"]),
                float(frame["worker_econ_count"]),
                float(frame["attack_count"]),
            ]
        )
    vector.extend(_one_hot(own["own_race"], RACES))
    vector.extend(_one_hot(observed_enemy["enemy_race"], RACES))
    vector.append(float(sample["game_time"]))
    prior_features = sample.get("_rule_prior_features", [])
    vector.extend(float(value) for value in prior_features)
    return vector


@dataclass(frozen=True)
class LabelEncoders:
    mappings: dict[str, dict[str, int]]

    @classmethod
    def from_samples(cls, samples: list[dict[str, Any]]) -> "LabelEncoders":
        mappings: dict[str, dict[str, int]] = {}
        for task in TASK_NAMES:
            values = sorted({str(sample[task]) for sample in samples})
            mappings[task] = {value: index for index, value in enumerate(values)}
        return cls(mappings=mappings)

    def encode(self, task: str, value: str) -> int:
        return self.mappings[task][str(value)]

    def decode(self, task: str, index: int) -> str:
        reverse = {idx: value for value, idx in self.mappings[task].items()}
        return reverse[index]

    def num_classes(self, task: str) -> int:
        return len(self.mappings[task])

    def to_json(self) -> dict[str, Any]:
        return self.mappings

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> "LabelEncoders":
        return cls(mappings={task: {str(k): int(v) for k, v in mapping.items()} for task, mapping in payload.items()})


def load_samples(path: Path) -> list[dict[str, Any]]:
    samples, errors = load_and_validate_jsonl(path)
    if errors:
        raise ValueError(f"invalid dataset split {path}: {errors}")
    return samples


class TeacherDataset(Dataset[dict[str, Tensor]]):
    def __init__(self, samples: list[dict[str, Any]], encoders: LabelEncoders) -> None:
        self.samples = samples
        self.encoders = encoders
        self._features = [torch.tensor(feature_vector(sample), dtype=torch.float32) for sample in samples]

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> dict[str, Tensor]:
        sample = self.samples[index]
        return {
            "features": self._features[index],
            "opening": torch.tensor(self.encoders.encode("enemy_opening_class", sample["enemy_opening_class"]), dtype=torch.long),
            "tech": torch.tensor(self.encoders.encode("enemy_tech_path", sample["enemy_tech_path"]), dtype=torch.long),
            "macro_action": torch.tensor(self.encoders.encode("macro_action_label", sample["macro_action_label"]), dtype=torch.long),
            "tempo": torch.tensor(self.encoders.encode("production_tempo_label", sample["production_tempo_label"]), dtype=torch.long),
            "future_winner": torch.tensor(self.encoders.encode("future_winner", sample["future_winner"]), dtype=torch.long),
            "future_game_length": torch.tensor(
                self.encoders.encode("future_game_length_bucket", sample["future_game_length_bucket"]), dtype=torch.long
            ),
            "future_pressure": torch.tensor(
                self.encoders.encode("future_pressure_proxy", sample["future_pressure_proxy"]), dtype=torch.long
            ),
        }


def save_label_encoders(path: Path, encoders: LabelEncoders) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(encoders.to_json(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
