from __future__ import annotations

import torch

from research.r7_world_model.models.action_conditioned_world_model import ActionConditionedWorldModel, ModelConfig


def test_action_conditioned_world_model_forward_shapes() -> None:
    cfg = ModelConfig(
        input_dim=40,
        hidden_dim=32,
        action_count=8,
        action_embed_dim=8,
        opening_classes=3,
        tech_classes=4,
        macro_action_classes=8,
        tempo_classes=3,
        future_winner_classes=2,
        game_length_classes=3,
        future_pressure_classes=2,
        use_action_conditioning=True,
    )
    model = ActionConditionedWorldModel(cfg)
    features = torch.randn(5, 40)
    action_index = torch.tensor([0, 1, 2, 3, 4])
    outputs = model(features, action_index)
    assert outputs["opening_logits"].shape == (5, 3)
    assert outputs["tech_logits"].shape == (5, 4)
    assert outputs["macro_action_logits"].shape == (5, 8)
    assert outputs["tempo_logits"].shape == (5, 3)
    assert outputs["future_winner_logits"].shape == (5, 2)
    assert outputs["future_game_length_logits"].shape == (5, 3)
    assert outputs["future_pressure_logits"].shape == (5, 2)
