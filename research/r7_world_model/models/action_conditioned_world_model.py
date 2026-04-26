from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class ModelConfig:
    input_dim: int
    hidden_dim: int
    action_count: int
    action_embed_dim: int
    opening_classes: int
    tech_classes: int
    macro_action_classes: int
    tempo_classes: int
    future_winner_classes: int
    game_length_classes: int
    future_pressure_classes: int
    use_action_conditioning: bool = True


class ActionConditionedWorldModel(nn.Module):
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.encoder = nn.Sequential(
            nn.Linear(cfg.input_dim, cfg.hidden_dim),
            nn.ReLU(),
            nn.Linear(cfg.hidden_dim, cfg.hidden_dim),
            nn.ReLU(),
        )
        self.action_head = nn.Linear(cfg.hidden_dim, cfg.macro_action_classes)
        self.action_embedding = nn.Embedding(cfg.action_count, cfg.action_embed_dim)

        self.opening_head = nn.Linear(cfg.hidden_dim, cfg.opening_classes)
        self.tech_head = nn.Linear(cfg.hidden_dim, cfg.tech_classes)
        self.tempo_head = nn.Linear(cfg.hidden_dim, cfg.tempo_classes)

        future_input_dim = cfg.hidden_dim + (cfg.action_embed_dim if cfg.use_action_conditioning else 0)
        self.future_winner_head = nn.Linear(future_input_dim, cfg.future_winner_classes)
        self.future_game_length_head = nn.Linear(future_input_dim, cfg.game_length_classes)
        self.future_pressure_head = nn.Linear(future_input_dim, cfg.future_pressure_classes)

    def encode(self, features: Tensor) -> Tensor:
        return self.encoder(features)

    def _future_features(self, state: Tensor, action_index: Tensor) -> Tensor:
        if not self.cfg.use_action_conditioning:
            return state
        action_embed = self.action_embedding(action_index)
        return torch.cat([state, action_embed], dim=-1)

    def forward(self, features: Tensor, action_index: Tensor | None = None) -> dict[str, Tensor]:
        state = self.encode(features)
        macro_action_logits = self.action_head(state)

        if action_index is None:
            action_index = macro_action_logits.argmax(dim=-1)

        future_features = self._future_features(state, action_index)
        return {
            "state": state,
            "opening_logits": self.opening_head(state),
            "tech_logits": self.tech_head(state),
            "macro_action_logits": macro_action_logits,
            "tempo_logits": self.tempo_head(state),
            "future_winner_logits": self.future_winner_head(future_features),
            "future_game_length_logits": self.future_game_length_head(future_features),
            "future_pressure_logits": self.future_pressure_head(future_features),
        }
