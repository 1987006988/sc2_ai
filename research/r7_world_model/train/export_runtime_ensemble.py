from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import torch

from research.r7_world_model.datasets.torch_dataset import load_samples
from research.r7_world_model.eval.baselines import build_rule_tables, build_static_prior


def _tensor_payload(checkpoint_path: Path) -> dict[str, Any]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    return {
        "variant_name": checkpoint["variant_name"],
        "model_config": checkpoint["model_config"],
        "label_encoders": checkpoint["label_encoders"],
        "state_dict": {
            key: value.detach().cpu().tolist()
            for key, value in checkpoint["state_dict"].items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a scratch-only R7 ensemble runtime payload.")
    parser.add_argument("--train-path", required=True, type=Path)
    parser.add_argument("--hidden-macro-checkpoint", required=True, type=Path)
    parser.add_argument("--future-checkpoint", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    train_samples = load_samples(args.train_path)
    global_priors = build_static_prior(train_samples)
    rule_tables = build_rule_tables(train_samples, global_priors)
    payload = {
        "runtime_id": "r7_world_model_runtime_v0",
        "selection_rule": "use scratch_no_action_ruleaug for hidden_state and macro_action groups; use scratch_full_ruleaug for future_proxy group",
        "claim_boundary": "scratch_only_runtime_export_no_warmstart_no_external_pretrained_model",
        "global_priors": global_priors,
        "rule_tables": rule_tables,
        "components": {
            "hidden_macro_arm": _tensor_payload(args.hidden_macro_checkpoint),
            "future_arm": _tensor_payload(args.future_checkpoint),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("R7_WORLD_MODEL_RUNTIME_EXPORTED")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
