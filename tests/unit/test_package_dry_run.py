import json

from evaluation.runner.package_dry_run import (
    EXCLUDED_PREFIXES,
    build_package_dry_run_manifest,
    write_package_dry_run_manifest,
)


def test_package_dry_run_manifest_checks_current_repo():
    manifest = build_package_dry_run_manifest(__import__("pathlib").Path("."))

    assert manifest.status == "ok"
    assert manifest.missing_required_paths == ()
    assert manifest.entrypoint == "src/sc2bot/main.py"
    assert "configs/bot/default.yaml" in manifest.config_paths
    assert "configs/maps/local_test_maps.yaml" in manifest.map_config_paths
    assert "scripts/setup/check_env.ps1" in manifest.script_paths
    assert "data/logs/" in manifest.excluded_prefixes
    assert "artifacts/reports/" in manifest.excluded_prefixes


def test_package_dry_run_manifest_reports_missing_required_paths(tmp_path):
    manifest = build_package_dry_run_manifest(tmp_path)

    assert manifest.status == "missing_required_paths"
    assert "src/sc2bot/main.py" in manifest.missing_required_paths
    assert manifest.excluded_prefixes == EXCLUDED_PREFIXES


def test_write_package_dry_run_manifest(tmp_path):
    manifest = build_package_dry_run_manifest(__import__("pathlib").Path("."))
    output = tmp_path / "manifest.json"

    write_package_dry_run_manifest(manifest, output)

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "ok"
    assert payload["entrypoint"] == "src/sc2bot/main.py"
