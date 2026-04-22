"""Build and merge real-match dataset manifests."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.metrics.schemas import ArtifactCompleteness, DatasetManifest


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact_completeness_from_payload(payload: dict[str, Any]) -> ArtifactCompleteness:
    return ArtifactCompleteness(**payload)


def merge_dataset_manifests(
    source_manifest_paths: list[Path],
    *,
    run_id: str,
    purpose: str,
    excluded_historical_dirs: tuple[str, ...] = (),
    created_at: str | None = None,
    min_match_count: int | None = None,
) -> DatasetManifest:
    """Merge scoped chunk manifests into one versioned dataset manifest."""

    if not source_manifest_paths:
        raise ValueError("at least one source manifest is required")

    included_match_dirs: list[str] = []
    evidence_paths: list[str] = []
    map_pool: set[str] = set()
    opponent_pool: set[str] = set()
    bot_configs: set[str] = set()
    chunk_run_ids: list[str] = []
    status_counts: Counter[str] = Counter()
    completeness = Counter(
        {
            "match_result_count": 0,
            "replay_count": 0,
            "telemetry_count": 0,
            "missing_match_result_count": 0,
            "missing_replay_count": 0,
            "missing_telemetry_count": 0,
        }
    )

    for manifest_path in source_manifest_paths:
        payload = _read_json(manifest_path)
        chunk_run_ids.append(str(payload["run_id"]))
        included_match_dirs.extend(str(path) for path in payload.get("included_match_dirs", ()))
        evidence_paths.extend(str(path) for path in payload.get("evidence_paths", ()))
        evidence_paths.append(str(manifest_path))
        map_pool.update(str(value) for value in payload.get("map_pool", ()))
        opponent_pool.update(str(value) for value in payload.get("opponent_pool", ()))
        bot_configs.update(str(value) for value in payload.get("bot_configs", ()))
        status_counts.update(payload.get("status_counts", {}))

        chunk_completeness = _artifact_completeness_from_payload(
            payload.get("artifact_completeness", {})
        )
        completeness.update(asdict(chunk_completeness))

    duplicates = sorted(
        match_dir
        for match_dir, count in Counter(included_match_dirs).items()
        if count > 1
    )
    if duplicates:
        raise ValueError(f"duplicate included match dirs: {duplicates}")

    match_count = len(included_match_dirs)
    if min_match_count is not None and match_count < min_match_count:
        raise ValueError(
            f"match_count {match_count} is below required minimum {min_match_count}"
        )

    manifest = DatasetManifest(
        run_id=run_id,
        created_at=created_at or datetime.now(timezone.utc).isoformat(),
        purpose=purpose,
        included_match_dirs=tuple(included_match_dirs),
        excluded_historical_dirs=excluded_historical_dirs,
        map_pool=tuple(sorted(map_pool)),
        opponent_pool=tuple(sorted(opponent_pool)),
        bot_configs=tuple(sorted(bot_configs)),
        config_snapshot={
            "source_manifests": tuple(str(path) for path in source_manifest_paths),
            "min_match_count": min_match_count,
            "merge_tool": "evaluation.metrics.dataset_manifest",
        },
        match_count=match_count,
        status_counts=dict(status_counts),
        artifact_completeness=ArtifactCompleteness(**dict(completeness)),
        evidence_paths=tuple(evidence_paths),
        chunk_run_ids=tuple(chunk_run_ids),
        source_manifests=tuple(str(path) for path in source_manifest_paths),
        notes=(
            "real baseline dataset manifest",
            "historical runs are excluded unless explicitly listed",
            "does not prove bot strength",
        ),
    )
    errors = manifest.validation_errors()
    if errors:
        raise ValueError(f"invalid merged dataset manifest: {errors}")
    return manifest


def write_dataset_manifest(manifest: DatasetManifest, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge real-match dataset manifests.")
    parser.add_argument("--source-manifest", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--excluded-historical-dir", action="append", default=[])
    parser.add_argument("--min-match-count", type=int, default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = merge_dataset_manifests(
        [Path(path) for path in args.source_manifest],
        run_id=args.run_id,
        purpose=args.purpose,
        excluded_historical_dirs=tuple(args.excluded_historical_dir),
        min_match_count=args.min_match_count,
    )
    write_dataset_manifest(manifest, Path(args.output))
    print(
        "dataset manifest generated: "
        f"{args.output} ({manifest.match_count} matches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
