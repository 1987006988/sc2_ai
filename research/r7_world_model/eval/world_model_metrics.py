from __future__ import annotations

from typing import Any

import torch
from torch import Tensor

from research.r7_world_model.eval.metrics import evaluate_predictions


def softmax_confidence(logits: Tensor) -> tuple[Tensor, Tensor]:
    probs = torch.softmax(logits, dim=-1)
    confidence, prediction = probs.max(dim=-1)
    return confidence, prediction


def expected_calibration_error(logits: Tensor, labels: Tensor, bins: int = 10) -> float:
    probs = torch.softmax(logits, dim=-1)
    confidence, predictions = probs.max(dim=-1)
    accuracy = predictions.eq(labels)
    ece = 0.0
    for idx in range(bins):
        lower = idx / bins
        upper = (idx + 1) / bins
        mask = (confidence > lower) & (confidence <= upper)
        if not mask.any():
            continue
        bucket_conf = confidence[mask].mean().item()
        bucket_acc = accuracy[mask].float().mean().item()
        ece += abs(bucket_conf - bucket_acc) * (mask.float().mean().item())
    return round(ece, 6)


def evaluate_task_from_logits(logits: Tensor, labels: Tensor, decoder: dict[int, str]) -> dict[str, Any]:
    confidence, predictions = softmax_confidence(logits)
    truth_strings = [decoder[int(index)] for index in labels.tolist()]
    pred_strings = [decoder[int(index)] for index in predictions.tolist()]
    metrics = evaluate_predictions(truth_strings, pred_strings)
    metrics["ece"] = expected_calibration_error(logits, labels)
    metrics["mean_confidence"] = round(confidence.mean().item(), 6)
    return metrics
