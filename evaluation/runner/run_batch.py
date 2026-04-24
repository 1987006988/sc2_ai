"""Run a minimal local evaluation loop using configured maps and opponent pool."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from evaluation.runner.collect_results import collect_results
from evaluation.runner.run_match import MatchRequest, run_match


def load_batch_config(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _load_yaml(path: str | Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _enabled_entries(path: str | Path, key: str) -> list[dict]:
    data = _load_yaml(path)
    return [item for item in data.get(key, []) if item.get("enabled", False)]


def _bot_config_entries(evaluation: dict) -> list[dict]:
    if "bot_configs" in evaluation:
        return [
            {
                "id": item["id"],
                "path": item["path"],
                "tags": tuple(item.get("tags", ())),
                "run_class": item.get("run_class", evaluation.get("run_class", "unspecified")),
                "validation_class": item.get(
                    "validation_class", evaluation.get("validation_class", "unspecified")
                ),
            }
            for item in evaluation["bot_configs"]
        ]
    return [
        {
            "id": "default",
            "path": evaluation["bot_config"],
            "tags": (),
            "run_class": evaluation.get("run_class", "unspecified"),
            "validation_class": evaluation.get("validation_class", "unspecified"),
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run smoke evaluation skeleton.")
    parser.add_argument("--config", default="configs/evaluation/smoke.yaml")
    args = parser.parse_args()
    config = load_batch_config(args.config)
    evaluation = config.get("evaluation", {})
    launch_mode = evaluation.get("launch_mode", "dry_run")
    bot_configs = _bot_config_entries(evaluation)
    repeats = int(evaluation.get("repeats", 1))
    maps = _enabled_entries(evaluation["maps_config"], "maps")
    opponents = _enabled_entries(evaluation["opponents_config"], "opponents")
    output_root = Path(evaluation["output_dir"])
    run_id = evaluation.get("run_id")
    if evaluation.get("isolate_runs", False):
        run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = output_root / run_id
    else:
        output_dir = output_root
    output_dir.mkdir(parents=True, exist_ok=True)

    for repeat_index in range(repeats):
        for bot_config in bot_configs:
            for map_item in maps:
                for opponent in opponents:
                    run_match(
                        MatchRequest(
                            bot_config=bot_config["path"],
                            bot_config_id=bot_config["id"],
                            bot_config_tags=bot_config["tags"] + (f"repeat_{repeat_index + 1}",),
                            map_id=map_item["id"],
                            map_name=map_item.get("name"),
                            map_file=map_item.get("file"),
                            opponent_id=opponent["id"],
                            opponent_type=opponent.get("type", "computer"),
                            opponent_race=opponent.get("race", "terran"),
                            opponent_difficulty=opponent.get("difficulty", "easy"),
                            opponent_tags=tuple(opponent.get("tags", ())),
                            output_dir=str(output_dir),
                            launch_mode=launch_mode,
                            run_class=bot_config["run_class"],
                            validation_class=bot_config["validation_class"],
                        )
                    )

    results = collect_results(output_dir)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "evaluation_name": evaluation.get("name", "unknown"),
                "run_id": run_id,
                "output_root": str(output_root),
                "output_dir": str(output_dir),
                "historical": False,
                "repeats": repeats,
                "launch_mode": launch_mode,
                "run_class": evaluation.get("run_class", "unspecified"),
                "validation_class": evaluation.get("validation_class", "unspecified"),
                "config_reference": str(Path(args.config)),
                "config_snapshot": config,
                "bot_configs": bot_configs,
                "maps": maps,
                "opponents": opponents,
                "matches": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"evaluation skeleton completed: {evaluation.get('name', 'unknown')} ({len(results)} matches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
