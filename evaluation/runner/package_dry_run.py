"""Dry-run package checks for ladder-like bot submission readiness."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_PATHS = (
    "pyproject.toml",
    "src/sc2bot/main.py",
    "configs/bot/default.yaml",
    "configs/maps/local_test_maps.yaml",
    "configs/opponents/local_pool.yaml",
    "configs/evaluation/smoke.yaml",
    "scripts/setup/check_env.ps1",
    "scripts/dev/run_smoke_eval.ps1",
)

EXCLUDED_PREFIXES = (
    "data/logs/",
    "data/replays/",
    "artifacts/reports/",
    "artifacts/models/",
    ".pytest_cache/",
    "__pycache__/",
)


@dataclass(frozen=True)
class PackageDryRunManifest:
    status: str
    repo_root: str
    entrypoint: str
    required_paths: tuple[str, ...]
    missing_required_paths: tuple[str, ...]
    config_paths: tuple[str, ...]
    map_config_paths: tuple[str, ...]
    script_paths: tuple[str, ...]
    excluded_prefixes: tuple[str, ...]
    notes: tuple[str, ...]


def build_package_dry_run_manifest(repo_root: Path) -> PackageDryRunManifest:
    root = repo_root.resolve()
    missing = tuple(path for path in REQUIRED_PATHS if not (root / path).exists())
    config_paths = tuple(sorted(str(path.relative_to(root)) for path in (root / "configs").glob("**/*.yaml")))
    map_config_paths = tuple(path for path in config_paths if path.startswith("configs/maps/"))
    script_paths = tuple(sorted(str(path.relative_to(root)) for path in (root / "scripts").glob("**/*") if path.is_file()))
    status = "ok" if not missing else "missing_required_paths"
    return PackageDryRunManifest(
        status=status,
        repo_root=str(root),
        entrypoint="src/sc2bot/main.py",
        required_paths=REQUIRED_PATHS,
        missing_required_paths=missing,
        config_paths=config_paths,
        map_config_paths=map_config_paths,
        script_paths=script_paths,
        excluded_prefixes=EXCLUDED_PREFIXES,
        notes=(
            "dry-run only; no upload performed",
            "dry-run only; no SC2 launch performed",
            "generated data/logs/artifacts paths are excluded by prefix policy",
        ),
    )


def write_package_dry_run_manifest(manifest: PackageDryRunManifest, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a package/upload dry-run check.")
    parser.add_argument("--repo-root", default=".", help="Repository root to inspect.")
    parser.add_argument(
        "--output",
        default="artifacts/package_dry_run/manifest.json",
        help="Path to write the dry-run manifest JSON.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = build_package_dry_run_manifest(Path(args.repo_root))
    write_package_dry_run_manifest(manifest, Path(args.output))
    print(json.dumps(asdict(manifest), ensure_ascii=False, indent=2))
    return 0 if manifest.status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
