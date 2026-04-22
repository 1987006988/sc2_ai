"""SC2 installation resolution and preflight checks."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


class SC2InstallationError(RuntimeError):
    """Raised when the SC2 installation path is missing or invalid."""


@dataclass(frozen=True)
class SC2Installation:
    root: Path
    versions_dir: Path
    support64_dir: Path
    sc2data_dir: Path
    executable: Path


@dataclass(frozen=True)
class SC2PreflightResult:
    ok: bool
    sc2path: str | None
    executable: str | None
    python_version: str
    message: str

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "sc2path": self.sc2path,
            "executable": self.executable,
            "python_version": self.python_version,
            "message": self.message,
        }


def resolve_sc2_installation_from_env(env_var: str = "SC2PATH") -> SC2Installation:
    raw = os.environ.get(env_var)
    if not raw:
        raise SC2InstallationError(
            f"{env_var} is not set. Set {env_var} to the StarCraft II root directory, "
            "for example: D:\\games\\StarCraft II"
        )

    root = Path(raw)
    if not root.exists():
        raise SC2InstallationError(f"{env_var} points to a missing path: {root}")
    if not root.is_dir():
        raise SC2InstallationError(f"{env_var} must point to a directory: {root}")

    versions_dir = root / "Versions"
    support64_dir = root / "Support64"
    sc2data_dir = root / "SC2Data"
    missing = [str(path.name) for path in (versions_dir, support64_dir, sc2data_dir) if not path.exists()]
    if missing:
        raise SC2InstallationError(
            f"SC2 installation at {root} is missing required entries: {', '.join(missing)}"
        )

    executable = root / "StarCraft II.exe"
    if not executable.exists():
        raise SC2InstallationError(f"StarCraft II executable not found at expected path: {executable}")

    return SC2Installation(
        root=root,
        versions_dir=versions_dir,
        support64_dir=support64_dir,
        sc2data_dir=sc2data_dir,
        executable=executable,
    )


def run_sc2_preflight(env_var: str = "SC2PATH") -> SC2PreflightResult:
    python_version = os.sys.version.split()[0]
    try:
        install = resolve_sc2_installation_from_env(env_var=env_var)
    except SC2InstallationError as exc:
        return SC2PreflightResult(
            ok=False,
            sc2path=os.environ.get(env_var),
            executable=None,
            python_version=python_version,
            message=str(exc),
        )

    return SC2PreflightResult(
        ok=True,
        sc2path=str(install.root),
        executable=str(install.executable),
        python_version=python_version,
        message="SC2 installation preflight passed.",
    )


def attempt_sc2_process_launch(
    installation: SC2Installation,
    timeout_seconds: float = 3.0,
) -> tuple[bool, str]:
    """Attempt to launch the SC2 executable and terminate it quickly.

    This is a minimal process-launch validation, not a real match startup.
    """

    process: subprocess.Popen[str] | None = None
    try:
        process = subprocess.Popen(
            [str(installation.executable)],
            cwd=str(installation.root),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        process.wait(timeout=timeout_seconds)
        return True, f"SC2 process launched and exited with code {process.returncode}."
    except subprocess.TimeoutExpired:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        return True, "SC2 process launch succeeded and was terminated after timeout."
    except Exception as exc:  # pragma: no cover - exercised through branch tests with monkeypatch
        return False, f"SC2 process launch failed: {exc}"
