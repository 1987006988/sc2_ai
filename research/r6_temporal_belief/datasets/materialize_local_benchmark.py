from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


GAS_STRUCTURES = {"assimilator", "extractor", "refinery"}
PRODUCTION_STRUCTURES = {
    "gateway",
    "barracks",
    "spawningpool",
    "roachwarren",
    "cyberneticscore",
    "barrackstechlab",
}
COMBAT_UNIT_SUPPLY = {
    "zergling": 1,
    "marine": 1,
    "zealot": 2,
    "roach": 2,
    "stalker": 2,
}


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_path(raw: str) -> Path:
    return Path(raw.replace("\\", "/"))


def _tech_hint(structures: list[str], gas_count: int, tech_signal: bool) -> str:
    structure_set = {s.lower() for s in structures}
    if "roachwarren" in structure_set:
        return "zerg_roach"
    if "cyberneticscore" in structure_set:
        return "protoss_core_tech"
    if "barrackstechlab" in structure_set:
        return "terran_bio_tech"
    if gas_count >= 2 or tech_signal:
        return "gas_tech"
    return "unknown"


def _estimate_army_supply(units: list[str]) -> int:
    return sum(COMBAT_UNIT_SUPPLY.get(unit.lower(), 1) for unit in units)


def _estimate_contact_risk(payload: dict[str, Any], army_supply: int, gas_count: int, prod_count: int) -> float:
    observation_confidence = float(payload.get("observation_confidence", 0.0))
    if bool(payload.get("possible_rush_signal")) or army_supply >= 4:
        return 0.85
    if army_supply > 0:
        return 0.65
    if bool(payload.get("possible_tech_signal")) and gas_count >= 1:
        return 0.45
    heuristic = 0.05 * gas_count + 0.08 * prod_count + observation_confidence
    return round(min(0.4, heuristic), 3)


def _compress_frames(frames: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not frames:
        return [{"game_time": 0.0}]
    compressed: list[dict[str, Any]] = []
    previous_signature: tuple[Any, ...] | None = None
    for idx, frame in enumerate(frames):
        signature = (
            frame.get("enemy_gas_structures"),
            frame.get("enemy_production_structures"),
            frame.get("enemy_visible_army_supply"),
            frame.get("enemy_contact_risk"),
            frame.get("enemy_contact_seen"),
            frame.get("enemy_expansion_seen"),
            frame.get("enemy_tech_path_hint"),
        )
        keep = previous_signature is None or signature != previous_signature or idx % 12 == 0 or idx == len(frames) - 1
        if keep:
            compressed.append(frame)
            previous_signature = signature
    return compressed


def _frames_from_telemetry(path: Path) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            event = json.loads(line)
            if event.get("event_type") != "scouting_observation":
                continue
            payload = event.get("payload", {})
            structures = [str(s).lower() for s in payload.get("seen_enemy_structures", [])]
            combat_units = [str(u).lower() for u in payload.get("seen_enemy_combat_units", [])]
            gas_count = sum(1 for s in structures if s in GAS_STRUCTURES)
            prod_count = sum(1 for s in structures if s in PRODUCTION_STRUCTURES)
            army_supply = _estimate_army_supply(combat_units)
            frame = {
                "game_time": float(payload.get("game_time", 0.0)),
                "enemy_gas_structures": gas_count,
                "enemy_production_structures": prod_count,
                "enemy_visible_army_supply": army_supply,
                "enemy_contact_risk": _estimate_contact_risk(payload, army_supply, gas_count, prod_count),
                "enemy_contact_seen": bool(combat_units),
                "enemy_expansion_seen": bool(payload.get("enemy_expansion_seen", False)),
                "enemy_tech_path_hint": _tech_hint(structures, gas_count, bool(payload.get("possible_tech_signal"))),
            }
            frames.append(frame)
    return _compress_frames(frames)


def _match_dirs_from_summary(summary_path: Path) -> list[Path]:
    payload = _load_json(summary_path)
    if "included_match_dirs" in payload:
        return [_normalize_path(raw) for raw in payload["included_match_dirs"]]
    dirs: list[Path] = []
    for result in payload.get("results", []):
        telemetry_path = result.get("telemetry_path")
        if not telemetry_path:
            continue
        dirs.append(_normalize_path(telemetry_path).parent.parent)
    return dirs


def _sample_from_match_dir(source_id: str, split_name: str, match_dir: Path) -> dict[str, Any]:
    match_result = _load_json(match_dir / "match_result.json")
    telemetry_path = match_dir / "telemetry" / "events.jsonl"
    frames = _frames_from_telemetry(telemetry_path)
    latest_observation: dict[str, Any] = {}
    with telemetry_path.open(encoding="utf-8") as handle:
        for line in handle:
            event = json.loads(line)
            if event.get("event_type") == "scouting_observation":
                latest_observation = event.get("payload", {})
    started_at = str(match_result.get("started_at", "unknown"))
    opponent_id = str(match_result.get("opponent_id", "unknown"))
    bot_config_id = str(match_result.get("bot_config_id", "unknown"))
    return {
        "replay_id": str(match_result.get("match_id", match_dir.name)),
        "replay_series_id": source_id,
        "player_identity": f"{opponent_id}:{bot_config_id}",
        "time_window_bucket": started_at[:10],
        "source_id": source_id,
        "split_name": split_name,
        "map_id": match_result.get("map_id"),
        "opponent_id": opponent_id,
        "opponent_race": match_result.get("opponent_race"),
        "latest_observation": latest_observation,
        "frames": frames,
    }


def _materialize_split(source_manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    source_manifest = _load_yaml(source_manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    split_samples: dict[str, list[dict[str, Any]]] = {"train": [], "val": [], "test": []}
    split_sources: dict[str, list[str]] = {"train": [], "val": [], "test": []}

    for source in source_manifest.get("sources", []):
        if source.get("source_type") != "local_historical_replay_corpus":
            continue
        if not bool(source.get("allowed_in_holdout_benchmark", False)):
            continue
        split_name = source.get("preferred_split")
        if split_name not in split_samples:
            continue
        summary_path = Path(str(source["summary_path"]))
        match_dirs = _match_dirs_from_summary(summary_path)
        split_sources[split_name].append(str(source["source_id"]))
        for match_dir in match_dirs:
            split_samples[split_name].append(_sample_from_match_dir(str(source["source_id"]), split_name, match_dir))

    written_paths: dict[str, str] = {}
    split_counts: dict[str, int] = {}
    for split_name, samples in split_samples.items():
        out_path = output_dir / f"{split_name}.jsonl"
        out_path.write_text(
            "\n".join(json.dumps(sample, ensure_ascii=False) for sample in samples) + ("\n" if samples else ""),
            encoding="utf-8",
        )
        written_paths[split_name] = str(out_path)
        split_counts[split_name] = len(samples)

    return {
        "materialized_split_paths": written_paths,
        "materialized_split_counts": split_counts,
        "materialized_split_sources": split_sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize R6 local historical benchmark inputs.")
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    result = _materialize_split(args.source_manifest, args.output_dir)
    print("R6_LOCAL_BENCHMARK_INPUTS_MATERIALIZED")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
