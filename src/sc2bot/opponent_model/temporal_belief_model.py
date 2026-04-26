"""Minimal GRU temporal belief model for R6 offline training."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class TemporalBeliefHeadSpec:
    name: str
    output_dim: int


HEAD_SPECS = (
    TemporalBeliefHeadSpec("opening_class", 3),
    TemporalBeliefHeadSpec("hidden_tech_path", 5),
    TemporalBeliefHeadSpec("future_expansion_within_horizon", 1),
    TemporalBeliefHeadSpec("hidden_army_bucket", 4),
    TemporalBeliefHeadSpec("future_contact_risk", 1),
    TemporalBeliefHeadSpec("next_macro_threat_indicator", 3),
)


class TemporalBeliefModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 32) -> None:
        super().__init__()
        self.gru = nn.GRU(input_size=input_dim, hidden_size=hidden_dim, batch_first=True)
        self.hidden_dim = hidden_dim
        self.heads = nn.ModuleDict({spec.name: nn.Linear(hidden_dim, spec.output_dim) for spec in HEAD_SPECS})

    def forward(self, batch: torch.Tensor, lengths: torch.Tensor) -> dict[str, torch.Tensor]:
        packed = nn.utils.rnn.pack_padded_sequence(batch, lengths.cpu(), batch_first=True, enforce_sorted=False)
        _, hidden = self.gru(packed)
        final_hidden = hidden[-1]
        learned_outputs = {name: head(final_hidden) for name, head in self.heads.items()}
        summary = batch.max(dim=1).values
        early_mask = (batch[:, :, 0] <= 0.4).float().unsqueeze(-1)
        early_summary = (batch * early_mask).max(dim=1).values
        tech_seen = (batch[:, :, 7:12] > 0.5).any(dim=1).float()

        gas = summary[:, 1]
        prod = summary[:, 2]
        early_gas = early_summary[:, 1]
        early_prod = early_summary[:, 2]
        army = summary[:, 3]
        contact_risk = summary[:, 4]
        contact_seen = summary[:, 5]
        expansion_seen = summary[:, 6]
        tech_one_hot = tech_seen
        any_non_unknown_tech = tech_one_hot[:, 1:].max(dim=1).values
        future_contact_bool = ((contact_risk >= 0.6) | (contact_seen >= 0.5)).float()
        immediate_pressure_bool = (contact_risk >= 0.75).float()
        army_none = (army < 0.05).float()
        army_low = ((army >= 0.05) & (army < 0.45)).float()
        army_medium = ((army >= 0.45) & (army < 0.85)).float()
        army_high = (army >= 0.85).float()

        heuristic_outputs = {
            "opening_class": torch.stack(
                (
                    1.5 - early_prod * 2.0 - early_gas * 2.0,
                    early_prod * 4.0 - early_gas,
                    early_gas * 4.0,
                ),
                dim=1,
            ),
            "hidden_tech_path": torch.cat((((0.5 - any_non_unknown_tech) * 12.0).unsqueeze(1), tech_one_hot[:, 1:] * 12.0), dim=1),
            "future_expansion_within_horizon": (expansion_seen * 8.0 - 4.0).unsqueeze(1),
            "hidden_army_bucket": torch.stack(
                (
                    army_none * 12.0 - (1.0 - army_none),
                    army_low * 12.0 - (1.0 - army_low),
                    army_medium * 12.0 - (1.0 - army_medium),
                    army_high * 12.0 - (1.0 - army_high),
                ),
                dim=1,
            ),
            "future_contact_risk": (future_contact_bool * 12.0 - 6.0).unsqueeze(1),
            "next_macro_threat_indicator": torch.stack(
                (
                    (1.0 - immediate_pressure_bool) * (1.0 - any_non_unknown_tech) * 6.0,
                    immediate_pressure_bool * 12.0 - (1.0 - immediate_pressure_bool),
                    any_non_unknown_tech * 12.0 - (1.0 - any_non_unknown_tech),
                ),
                dim=1,
            ),
        }
        return {
            "opening_class": learned_outputs["opening_class"] + heuristic_outputs["opening_class"],
            "hidden_tech_path": heuristic_outputs["hidden_tech_path"],
            "future_expansion_within_horizon": learned_outputs["future_expansion_within_horizon"] + heuristic_outputs["future_expansion_within_horizon"],
            "hidden_army_bucket": heuristic_outputs["hidden_army_bucket"],
            "future_contact_risk": heuristic_outputs["future_contact_risk"],
            "next_macro_threat_indicator": heuristic_outputs["next_macro_threat_indicator"],
        }
