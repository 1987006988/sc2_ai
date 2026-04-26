from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import torch
import yaml
from torch import nn

from research.r6_temporal_belief.datasets.reader import load_and_validate_jsonl
from research.r6_temporal_belief.eval.metrics import evaluate_prediction_bundle
from research.r6_temporal_belief.eval.offline_baselines import label_dict, rule_based_predictor, static_prior_predictor, build_static_prior
from sc2bot.opponent_model.feature_encoder import build_padded_batch
from sc2bot.opponent_model.temporal_belief_model import TemporalBeliefModel


OPENING_LABELS = ("econ_opening", "production_opening", "gas_opening")
TECH_LABELS = ("unknown", "gas_tech", "terran_bio_tech", "protoss_core_tech", "zerg_roach")
ARMY_LABELS = ("none", "low", "medium", "high")
THREAT_LABELS = ("standard_pressure", "immediate_pressure", "tech_transition")


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_split(path: Path) -> list[dict[str, Any]]:
    samples, errors = load_and_validate_jsonl(path)
    if errors:
        raise ValueError(f"invalid split {path}: {errors}")
    return samples


def _label_index(value: str | bool, labels: tuple[str, ...] | None = None) -> int:
    if isinstance(value, bool):
        return int(value)
    assert labels is not None
    return labels.index(value) if value in labels else 0


def _build_targets(samples: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
    truths = [label_dict(sample) for sample in samples]
    return {
        "opening_class": torch.tensor([_label_index(row["opening_class"], OPENING_LABELS) for row in truths], dtype=torch.long),
        "hidden_tech_path": torch.tensor([_label_index(row["hidden_tech_path"], TECH_LABELS) for row in truths], dtype=torch.long),
        "future_expansion_within_horizon": torch.tensor([float(row["future_expansion_within_horizon"]) for row in truths], dtype=torch.float32),
        "hidden_army_bucket": torch.tensor([_label_index(row["hidden_army_bucket"], ARMY_LABELS) for row in truths], dtype=torch.long),
        "future_contact_risk": torch.tensor([float(row["future_contact_risk"]) for row in truths], dtype=torch.float32),
        "next_macro_threat_indicator": torch.tensor([_label_index(row["next_macro_threat_indicator"], THREAT_LABELS) for row in truths], dtype=torch.long),
    }


def _loss_fn(outputs: dict[str, torch.Tensor], targets: dict[str, torch.Tensor]) -> torch.Tensor:
    ce = nn.CrossEntropyLoss()
    bce = nn.BCEWithLogitsLoss()
    return (
        ce(outputs["opening_class"], targets["opening_class"])
        + ce(outputs["hidden_tech_path"], targets["hidden_tech_path"])
        + bce(outputs["future_expansion_within_horizon"].squeeze(-1), targets["future_expansion_within_horizon"])
        + ce(outputs["hidden_army_bucket"], targets["hidden_army_bucket"])
        + bce(outputs["future_contact_risk"].squeeze(-1), targets["future_contact_risk"])
        + ce(outputs["next_macro_threat_indicator"], targets["next_macro_threat_indicator"])
    )


def _outputs_to_predictions(outputs: dict[str, torch.Tensor]) -> list[dict[str, Any]]:
    opening_idx = torch.argmax(outputs["opening_class"], dim=1).tolist()
    tech_idx = torch.argmax(outputs["hidden_tech_path"], dim=1).tolist()
    expand = (torch.sigmoid(outputs["future_expansion_within_horizon"].squeeze(-1)) >= 0.5).tolist()
    army_idx = torch.argmax(outputs["hidden_army_bucket"], dim=1).tolist()
    contact = (torch.sigmoid(outputs["future_contact_risk"].squeeze(-1)) >= 0.5).tolist()
    threat_idx = torch.argmax(outputs["next_macro_threat_indicator"], dim=1).tolist()
    predictions: list[dict[str, Any]] = []
    for i in range(len(opening_idx)):
        predictions.append(
            {
                "opening_class": OPENING_LABELS[opening_idx[i]],
                "hidden_tech_path": TECH_LABELS[tech_idx[i]],
                "future_expansion_within_horizon": bool(expand[i]),
                "hidden_army_bucket": ARMY_LABELS[army_idx[i]],
                "future_contact_risk": bool(contact[i]),
                "next_macro_threat_indicator": THREAT_LABELS[threat_idx[i]],
            }
        )
    return predictions


def _evaluate_model(model: TemporalBeliefModel, samples: list[dict[str, Any]]) -> dict[str, Any]:
    model.eval()
    batch, lengths = build_padded_batch(samples)
    with torch.no_grad():
        outputs = model(batch, lengths)
    truths = [label_dict(sample) for sample in samples]
    predictions = _outputs_to_predictions(outputs)
    return evaluate_prediction_bundle(truths, predictions)


def _mean_balanced_accuracy(report: dict[str, dict[str, float]], primary_tasks: list[str]) -> float:
    return sum(report[task]["balanced_accuracy"] for task in primary_tasks) / len(primary_tasks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Train the R6 GRU temporal belief model.")
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    cfg = _load_yaml(args.config)
    train_samples = _load_split(Path(cfg["data"]["train_path"]))
    val_samples = _load_split(Path(cfg["data"]["val_path"]))
    test_samples = _load_split(Path(cfg["data"]["test_path"]))

    train_batch, train_lengths = build_padded_batch(train_samples)
    train_targets = _build_targets(train_samples)

    input_dim = train_batch.shape[-1]
    hidden_dim = int(cfg["model"].get("hidden_dim", 32))
    epochs = int(cfg["train"].get("epochs", 80))
    lr = float(cfg["train"].get("learning_rate", 0.01))
    primary_tasks = list(cfg["eval"]["primary_task_bundle"])

    model = TemporalBeliefModel(input_dim=input_dim, hidden_dim=hidden_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    best_val_score = -1.0
    best_state = None
    history: list[dict[str, float]] = []

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(train_batch, train_lengths)
        loss = _loss_fn(outputs, train_targets)
        loss.backward()
        optimizer.step()

        val_report = _evaluate_model(model, val_samples)
        val_score = _mean_balanced_accuracy(val_report, primary_tasks)
        history.append({"epoch": epoch + 1, "loss": round(float(loss.item()), 6), "val_score": round(val_score, 6)})
        if val_score > best_val_score:
            best_val_score = val_score
            best_state = {k: v.detach().cpu() for k, v in model.state_dict().items()}

    if best_state is None:
        raise RuntimeError("training produced no checkpoint state")

    model.load_state_dict(best_state)
    val_report = _evaluate_model(model, val_samples)
    test_report = _evaluate_model(model, test_samples)
    priors = build_static_prior(train_samples)
    static_val = evaluate_prediction_bundle([label_dict(s) for s in val_samples], [static_prior_predictor(priors, s) for s in val_samples])
    static_test = evaluate_prediction_bundle([label_dict(s) for s in test_samples], [static_prior_predictor(priors, s) for s in test_samples])
    rule_val = evaluate_prediction_bundle([label_dict(s) for s in val_samples], [rule_based_predictor(s) for s in val_samples])
    rule_test = evaluate_prediction_bundle([label_dict(s) for s in test_samples], [rule_based_predictor(s) for s in test_samples])

    checkpoint_path = Path(cfg["artifacts"]["checkpoint_path"])
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "config_path": str(args.config),
            "best_val_score": best_val_score,
            "hidden_dim": hidden_dim,
        },
        checkpoint_path,
    )

    result = {
        "model_name": "temporal_gru_v0",
        "checkpoint_path": str(checkpoint_path),
        "history": history,
        "primary_task_bundle": primary_tasks,
        "comparators": {
            "learned_temporal": {
                "val": val_report,
                "test": test_report,
            },
            "rule_based_runtime_aligned": {
                "val": rule_val,
                "test": rule_test,
            },
            "static_prior": {
                "val": static_val,
                "test": static_test,
            },
        },
        "aggregate_scores": {
            "learned_temporal_val": _mean_balanced_accuracy(val_report, primary_tasks),
            "learned_temporal_test": _mean_balanced_accuracy(test_report, primary_tasks),
            "rule_based_val": _mean_balanced_accuracy(rule_val, primary_tasks),
            "rule_based_test": _mean_balanced_accuracy(rule_test, primary_tasks),
            "static_prior_val": _mean_balanced_accuracy(static_val, primary_tasks),
            "static_prior_test": _mean_balanced_accuracy(static_test, primary_tasks),
        },
    }

    output_path = Path(cfg["artifacts"]["results_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R6_TEMPORAL_MODEL_TRAINED")
    print(f"checkpoint={checkpoint_path}")
    print(f"results={output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
