from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader
import yaml

from research.r7_world_model.datasets.torch_dataset import (
    LabelEncoders,
    TeacherDataset,
    TASK_NAMES,
    load_samples,
    save_label_encoders,
)
from research.r7_world_model.eval.baselines import build_rule_tables, build_static_prior, rule_based_predictor
from research.r7_world_model.eval.world_model_metrics import evaluate_task_from_logits
from research.r7_world_model.models.action_conditioned_world_model import ActionConditionedWorldModel, ModelConfig


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _decoder(encoders: LabelEncoders, task: str) -> dict[int, str]:
    return {index: value for value, index in encoders.mappings[task].items()}


def _collect_outputs(model: ActionConditionedWorldModel, loader: DataLoader, device: torch.device) -> dict[str, Any]:
    model.eval()
    outputs: dict[str, list[torch.Tensor]] = {
        "opening_logits": [],
        "tech_logits": [],
        "macro_action_logits": [],
        "tempo_logits": [],
        "future_winner_logits": [],
        "future_game_length_logits": [],
        "future_pressure_logits": [],
        "opening": [],
        "tech": [],
        "macro_action": [],
        "tempo": [],
        "future_winner": [],
        "future_game_length": [],
        "future_pressure": [],
    }
    with torch.no_grad():
        for batch in loader:
            features = batch["features"].to(device)
            teacher_actions = batch["macro_action"].to(device)
            prediction = model(features, teacher_actions)
            for key in (
                "opening_logits",
                "tech_logits",
                "macro_action_logits",
                "tempo_logits",
                "future_winner_logits",
                "future_game_length_logits",
                "future_pressure_logits",
            ):
                outputs[key].append(prediction[key].cpu())
            for key in ("opening", "tech", "macro_action", "tempo", "future_winner", "future_game_length", "future_pressure"):
                outputs[key].append(batch[key].cpu())
    return {key: torch.cat(values, dim=0) for key, values in outputs.items()}


def _score_outputs(outputs: dict[str, torch.Tensor], encoders: LabelEncoders) -> dict[str, Any]:
    task_specs = {
        "enemy_opening_class": ("opening_logits", "opening"),
        "enemy_tech_path": ("tech_logits", "tech"),
        "macro_action_label": ("macro_action_logits", "macro_action"),
        "production_tempo_label": ("tempo_logits", "tempo"),
        "future_winner": ("future_winner_logits", "future_winner"),
        "future_game_length_bucket": ("future_game_length_logits", "future_game_length"),
        "future_pressure_proxy": ("future_pressure_logits", "future_pressure"),
    }
    task_metrics: dict[str, Any] = {}
    for task, (logit_key, label_key) in task_specs.items():
        task_metrics[task] = evaluate_task_from_logits(outputs[logit_key], outputs[label_key], _decoder(encoders, task))

    groups = {
        "hidden_state": ("enemy_opening_class", "enemy_tech_path"),
        "macro_action": ("macro_action_label", "production_tempo_label"),
        "future_proxy": ("future_winner", "future_game_length_bucket", "future_pressure_proxy"),
    }
    group_scores = {
        group: round(sum(task_metrics[task]["balanced_accuracy"] for task in tasks) / len(tasks), 6)
        for group, tasks in groups.items()
    }
    mean_ece = round(sum(task_metrics[task]["ece"] for task in task_specs) / len(task_specs), 6)
    return {
        "tasks": task_metrics,
        "group_balanced_accuracy": group_scores,
        "aggregate_balanced_accuracy": round(sum(group_scores.values()) / len(group_scores), 6),
        "mean_ece": mean_ece,
    }


def train_variant(
    train_path: Path,
    val_path: Path,
    test_path: Path,
    output_dir: Path,
    variant_name: str,
    hidden_dim: int,
    lr: float,
    epochs: int,
    seed: int,
    use_action_conditioning: bool,
    include_rule_priors: bool = False,
) -> dict[str, Any]:
    set_seed(seed)
    train_samples = load_samples(train_path)
    val_samples = load_samples(val_path)
    test_samples = load_samples(test_path)
    global_priors = build_static_prior(train_samples)
    rule_tables = build_rule_tables(train_samples, global_priors)

    if include_rule_priors:
        def attach_rule_prior_features(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
            enriched: list[dict[str, Any]] = []
            for sample in samples:
                row = dict(sample)
                priors = rule_based_predictor(sample, global_priors, rule_tables)
                row["_rule_priors"] = priors
                enriched.append(row)
            return enriched

        train_samples = attach_rule_prior_features(train_samples)
        val_samples = attach_rule_prior_features(val_samples)
        test_samples = attach_rule_prior_features(test_samples)

    encoders = LabelEncoders.from_samples(train_samples + val_samples + test_samples)
    if include_rule_priors:
        def encode_rule_priors(samples: list[dict[str, Any]]) -> None:
            for sample in samples:
                priors = sample["_rule_priors"]
                features: list[float] = []
                for task in TASK_NAMES:
                    predicted = priors[task]
                    count = encoders.num_classes(task)
                    index = encoders.encode(task, predicted)
                    features.extend(1.0 if idx == index else 0.0 for idx in range(count))
                sample["_rule_prior_features"] = features

        encode_rule_priors(train_samples)
        encode_rule_priors(val_samples)
        encode_rule_priors(test_samples)

    train_dataset = TeacherDataset(train_samples, encoders)
    val_dataset = TeacherDataset(val_samples, encoders)
    test_dataset = TeacherDataset(test_samples, encoders)

    input_dim = train_dataset[0]["features"].shape[0]
    model_cfg = ModelConfig(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        action_count=encoders.num_classes("macro_action_label"),
        action_embed_dim=8,
        opening_classes=encoders.num_classes("enemy_opening_class"),
        tech_classes=encoders.num_classes("enemy_tech_path"),
        macro_action_classes=encoders.num_classes("macro_action_label"),
        tempo_classes=encoders.num_classes("production_tempo_label"),
        future_winner_classes=encoders.num_classes("future_winner"),
        game_length_classes=encoders.num_classes("future_game_length_bucket"),
        future_pressure_classes=encoders.num_classes("future_pressure_proxy"),
        use_action_conditioning=use_action_conditioning,
    )
    model = ActionConditionedWorldModel(model_cfg)
    device = torch.device("cpu")
    model.to(device)
    optimizer = Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    train_loader = DataLoader(train_dataset, batch_size=len(train_dataset), shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=len(val_dataset), shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=len(test_dataset), shuffle=False)

    best_state: dict[str, Any] | None = None
    best_val = -1.0
    history: list[dict[str, Any]] = []
    for epoch in range(1, epochs + 1):
        model.train()
        for batch in train_loader:
            optimizer.zero_grad()
            features = batch["features"].to(device)
            teacher_actions = batch["macro_action"].to(device)
            outputs = model(features, teacher_actions)
            loss = (
                criterion(outputs["opening_logits"], batch["opening"].to(device))
                + criterion(outputs["tech_logits"], batch["tech"].to(device))
                + criterion(outputs["macro_action_logits"], batch["macro_action"].to(device))
                + criterion(outputs["tempo_logits"], batch["tempo"].to(device))
                + criterion(outputs["future_winner_logits"], batch["future_winner"].to(device))
                + criterion(outputs["future_game_length_logits"], batch["future_game_length"].to(device))
                + criterion(outputs["future_pressure_logits"], batch["future_pressure"].to(device))
            )
            loss.backward()
            optimizer.step()
        val_outputs = _collect_outputs(model, val_loader, device)
        val_score = _score_outputs(val_outputs, encoders)
        history.append({"epoch": epoch, "val_aggregate_balanced_accuracy": val_score["aggregate_balanced_accuracy"]})
        if val_score["aggregate_balanced_accuracy"] > best_val:
            best_val = val_score["aggregate_balanced_accuracy"]
            best_state = {"model": model.state_dict(), "val_score": val_score, "epoch": epoch}

    if best_state is None:
        raise RuntimeError("training did not produce a best state")

    model.load_state_dict(best_state["model"])
    val_outputs = _collect_outputs(model, val_loader, device)
    test_outputs = _collect_outputs(model, test_loader, device)
    val_score = _score_outputs(val_outputs, encoders)
    test_score = _score_outputs(test_outputs, encoders)

    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / f"{variant_name}.pt"
    torch.save(
        {
            "variant_name": variant_name,
            "seed": seed,
            "model_config": asdict(model_cfg),
            "label_encoders": encoders.to_json(),
            "state_dict": model.state_dict(),
            "best_epoch": best_state["epoch"],
        },
        checkpoint_path,
    )
    encoders_path = output_dir / f"{variant_name}_label_encoders.json"
    save_label_encoders(encoders_path, encoders)

    return {
        "variant_name": variant_name,
        "seed": seed,
        "checkpoint_path": str(checkpoint_path),
        "label_encoders_path": str(encoders_path),
        "best_epoch": best_state["epoch"],
        "history": history,
        "model_config": asdict(model_cfg),
        "use_action_conditioning": use_action_conditioning,
        "include_rule_priors": include_rule_priors,
        "splits": {
            "val": val_score,
            "test": test_score,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Train the R7 action-conditioned world model.")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--variant", default="scratch_full")
    parser.add_argument("--no-action-conditioning", action="store_true")
    parser.add_argument("--include-rule-priors", action="store_true")
    parser.add_argument("--output-json", type=Path, default=None)
    args = parser.parse_args()

    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    output_dir = Path(config["output_dir"])
    results = train_variant(
        train_path=Path(config["train_path"]),
        val_path=Path(config["val_path"]),
        test_path=Path(config["test_path"]),
        output_dir=output_dir,
        variant_name=args.variant,
        hidden_dim=int(config["hidden_dim"]),
        lr=float(config["learning_rate"]),
        epochs=int(config["epochs"]),
        seed=int(config["seed"]),
        use_action_conditioning=not args.no_action_conditioning,
        include_rule_priors=args.include_rule_priors,
    )
    output_json = args.output_json or (output_dir / f"{args.variant}.json")
    output_json.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R7_WORLD_MODEL_TRAINED")
    print(f"variant={args.variant}")
    print(f"output={output_json}")
    print(f"test_aggregate={results['splits']['test']['aggregate_balanced_accuracy']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
