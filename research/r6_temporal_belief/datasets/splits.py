from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_source_manifest(source_manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids: set[str] = set()
    for source in source_manifest.get("sources", []):
        source_id = source.get("source_id")
        if not source_id:
            errors.append("missing source_id")
            continue
        if source_id in source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        source_ids.add(source_id)
        if "intended_use" not in source:
            errors.append(f"missing intended_use: {source_id}")
        if source.get("source_type") == "local_accepted_replay_artifacts" and source.get(
            "allowed_in_holdout_benchmark", True
        ):
            errors.append(f"local accepted artifacts cannot enter holdout benchmark: {source_id}")
    return errors


def validate_dataset_manifest(dataset_manifest: dict[str, Any], source_manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    known_sources = {source["source_id"] for source in source_manifest.get("sources", []) if source.get("source_id")}
    for source in dataset_manifest.get("sources", []):
        source_id = source.get("source_id")
        if source_id not in known_sources:
            errors.append(f"dataset manifest references unknown source: {source_id}")
    splits = dataset_manifest.get("splits", {})
    for split_name in ("train", "val", "test"):
        if split_name not in splits:
            errors.append(f"missing split section: {split_name}")
        elif splits[split_name].get("status") == "materialized" and "path" not in splits[split_name]:
            errors.append(f"materialized split missing path: {split_name}")
    if "local_accepted_replay_artifacts_into_holdout_benchmark" not in dataset_manifest.get(
        "forbidden_mixes", []
    ):
        errors.append("forbidden_mixes missing local accepted holdout exclusion")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate R6 replay source and split contracts.")
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--dataset-manifest", required=True, type=Path)
    args = parser.parse_args()

    source_manifest = load_yaml(args.source_manifest)
    dataset_manifest = load_json(args.dataset_manifest)
    errors = []
    errors.extend(validate_source_manifest(source_manifest))
    errors.extend(validate_dataset_manifest(dataset_manifest, source_manifest))

    if errors:
        print("R6_DATASET_CONTRACT_INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    print("R6_DATASET_CONTRACT_VALID")
    print(f"source_manifest={args.source_manifest}")
    print(f"dataset_manifest={args.dataset_manifest}")
    print(f"sources={len(source_manifest.get('sources', []))}")
    print(f"split_policy={dataset_manifest.get('split_policy_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
