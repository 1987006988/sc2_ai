from pathlib import Path

import pytest

from sc2bot.runtime.sc2_installation import (
    SC2InstallationError,
    resolve_sc2_installation_from_env,
    run_sc2_preflight,
)


def _make_sc2_root(root: Path) -> Path:
    (root / "Versions").mkdir(parents=True)
    (root / "Support64").mkdir(parents=True)
    (root / "SC2Data").mkdir(parents=True)
    (root / "StarCraft II.exe").write_text("stub", encoding="utf-8")
    return root


def test_resolve_sc2_installation_from_env_success(tmp_path, monkeypatch):
    root = _make_sc2_root(tmp_path / "StarCraft II")
    monkeypatch.setenv("SC2PATH", str(root))

    installation = resolve_sc2_installation_from_env()

    assert installation.root == root
    assert installation.versions_dir.exists()
    assert installation.support64_dir.exists()
    assert installation.sc2data_dir.exists()


def test_resolve_sc2_installation_from_env_missing_env(monkeypatch):
    monkeypatch.delenv("SC2PATH", raising=False)

    with pytest.raises(SC2InstallationError) as exc:
        resolve_sc2_installation_from_env()

    assert "SC2PATH is not set" in str(exc.value)


def test_resolve_sc2_installation_from_env_missing_required_dir(tmp_path, monkeypatch):
    root = tmp_path / "StarCraft II"
    root.mkdir()
    (root / "Versions").mkdir()
    (root / "SC2Data").mkdir()
    (root / "StarCraft II.exe").write_text("stub", encoding="utf-8")
    monkeypatch.setenv("SC2PATH", str(root))

    with pytest.raises(SC2InstallationError) as exc:
        resolve_sc2_installation_from_env()

    assert "Support64" in str(exc.value)


def test_run_sc2_preflight_reports_missing_env(monkeypatch):
    monkeypatch.delenv("SC2PATH", raising=False)

    result = run_sc2_preflight()

    assert result.ok is False
    assert "SC2PATH is not set" in result.message
