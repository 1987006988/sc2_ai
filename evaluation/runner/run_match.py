"""Run one local dry-run match and persist minimal results."""

from __future__ import annotations

import json
import math
import os
import sys
import traceback
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sc2bot.config.loader import load_bot_config
from sc2bot.config.schema import RuntimeConfig, TelemetryConfig
from sc2bot.runtime.bot_app import BotApp
from sc2bot.runtime.game_loop import build_python_sc2_local_bot
from sc2bot.runtime.sc2_installation import (
    SC2Installation,
    SC2InstallationError,
    resolve_sc2_installation_from_env,
    run_sc2_preflight,
)

from evaluation.metrics.schemas import MatchResult

SC2_GAME_LOOPS_PER_SECOND = 22.4
SC2_RUN_GAME_MIN_TIME_LIMIT_SECONDS = 120
SC2_RUN_GAME_TIME_LIMIT_BUFFER_SECONDS = 30


@dataclass(frozen=True)
class MatchRequest:
    bot_config: str
    map_id: str
    bot_config_id: str = "default"
    bot_config_tags: tuple[str, ...] = ()
    map_name: str | None = None
    map_file: str | None = None
    opponent_id: str = "builtin_easy_terran"
    opponent_type: str = "computer"
    opponent_race: str = "terran"
    opponent_difficulty: str = "easy"
    opponent_tags: tuple[str, ...] = ()
    output_dir: str = "data/logs/evaluation"
    launch_mode: str = "dry_run"


def _game_time_limit_seconds(runtime_config: RuntimeConfig) -> int:
    """Convert bot runtime loop limit into python-sc2 run_game seconds."""

    runtime_seconds = math.ceil(runtime_config.max_game_loop / SC2_GAME_LOOPS_PER_SECOND)
    return max(
        SC2_RUN_GAME_MIN_TIME_LIMIT_SECONDS,
        runtime_seconds + SC2_RUN_GAME_TIME_LIMIT_BUFFER_SECONDS,
    )


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _race_from_str(name: str) -> Any:
    from sc2.data import Race

    mapping = {
        "protoss": Race.Protoss,
        "terran": Race.Terran,
        "zerg": Race.Zerg,
        "random": Race.Random,
    }
    key = name.strip().lower()
    if key not in mapping:
        raise ValueError(f"Unsupported race for local match launch: {name}")
    return mapping[key]


def _difficulty_from_str(name: str) -> Any:
    from sc2.data import Difficulty

    mapping = {
        "veryeasy": Difficulty.VeryEasy,
        "easy": Difficulty.Easy,
        "medium": Difficulty.Medium,
        "mediumhard": Difficulty.MediumHard,
        "hard": Difficulty.Hard,
        "harder": Difficulty.Harder,
        "veryhard": Difficulty.VeryHard,
        "cheatvision": Difficulty.CheatVision,
        "cheatmoney": Difficulty.CheatMoney,
        "cheatinsane": Difficulty.CheatInsane,
    }
    key = name.strip().lower()
    if key not in mapping:
        raise ValueError(f"Unsupported difficulty for local match launch: {name}")
    return mapping[key]


def _resolve_map_path(installation: SC2Installation, request: MatchRequest) -> Path:
    maps_dir = installation.root / "Maps"
    if not maps_dir.exists():
        raise SC2InstallationError(f"SC2 Maps directory is missing: {maps_dir}")
    if not request.map_file:
        raise SC2InstallationError(
            f"Map config for '{request.map_id}' is missing the .SC2Map file entry."
        )
    map_path = maps_dir / request.map_file
    if not map_path.exists():
        raise SC2InstallationError(f"Configured map file does not exist: {map_path}")
    return map_path


def _existing_sc2_base_executables(installation: SC2Installation) -> list[tuple[int, Path]]:
    versions_dir = installation.root / "Versions"
    if not versions_dir.exists():
        return []
    candidates: list[tuple[int, Path]] = []
    for base_dir in versions_dir.iterdir():
        if not base_dir.is_dir() or not base_dir.name.startswith("Base"):
            continue
        try:
            base_version = int(base_dir.name[4:])
        except ValueError:
            continue
        executable = base_dir / "SC2_x64.exe"
        if executable.exists():
            candidates.append((base_version, executable))
    return sorted(candidates)


def _patch_python_sc2_launch_paths(
    installation: SC2Installation,
    diagnostics_path: Path,
) -> dict[str, Any]:
    from sc2.paths import Paths

    default_executable = Path(Paths.EXECUTABLE)
    default_cwd = Path(Paths.CWD) if Paths.CWD else None
    selected_executable = default_executable
    selected_base_version: int | None = None
    patched = False

    candidates = _existing_sc2_base_executables(installation)
    if not default_executable.exists() and candidates:
        selected_base_version, selected_executable = candidates[-1]
        Paths.EXECUTABLE = selected_executable
        Paths.CWD = installation.root / "Support64"
        patched = True

    payload = {
        "default_executable": str(default_executable),
        "default_executable_exists": default_executable.exists(),
        "default_cwd": str(default_cwd) if default_cwd else None,
        "default_cwd_exists": default_cwd.exists() if default_cwd else None,
        "candidate_executables": [
            {"base_version": version, "executable": str(executable)}
            for version, executable in candidates
        ],
        "selected_executable": str(selected_executable),
        "selected_executable_exists": selected_executable.exists(),
        "selected_base_version": selected_base_version,
        "patched_python_sc2_paths": patched,
        "selected_cwd": str(Paths.CWD) if Paths.CWD else None,
    }
    _write_json(diagnostics_path, payload)
    return payload


def _build_bot_app(request: MatchRequest, telemetry_dir: Path) -> BotApp:
    bot_config = load_bot_config(request.bot_config)
    bot_config = replace(
        bot_config,
        telemetry=TelemetryConfig(
            enabled=True,
            output_dir=str(telemetry_dir),
            verbose=bot_config.telemetry.verbose,
        ),
    )
    return BotApp.from_bot_config(bot_config)


def _run_python_sc2_local_game(
    request: MatchRequest,
    app: BotApp,
    installation: SC2Installation,
    replay_path: Path,
) -> str:
    _resolve_map_path(installation, request)

    from sc2 import maps
    from sc2.main import run_game
    from sc2.player import Bot, Computer

    _patch_python_sc2_launch_paths(
        installation,
        replay_path.parent / "launch_path_diagnostics.json",
    )

    map_name = request.map_name or request.map_id
    bot_player = Bot(
        _race_from_str(app.config.bot.race),
        build_python_sc2_local_bot(
            app.container,
            app.config.bot.name,
            app.config.runtime,
            app.config.build_order,
        ),
        name=app.config.bot.name,
    )
    if request.opponent_type != "computer":
        raise ValueError(
            f"Unsupported opponent type for phase-1 local match: {request.opponent_type}"
        )
    opponent_player = Computer(
        _race_from_str(request.opponent_race),
        _difficulty_from_str(request.opponent_difficulty),
    )
    result = run_game(
        maps.get(map_name),
        [bot_player, opponent_player],
        realtime=False,
        save_replay_as=str(replay_path),
        game_time_limit=_game_time_limit_seconds(app.config.runtime),
    )
    return str(result)


def _write_launch_error_diagnostics(
    output_dir: Path,
    exc: Exception,
    request: MatchRequest,
    installation: SC2Installation,
    replay_path: Path,
) -> None:
    map_path: str | None
    try:
        map_path = str(_resolve_map_path(installation, request))
    except Exception as map_exc:
        map_path = f"unresolved: {map_exc}"
    diagnostics = {
        "exception_type": type(exc).__name__,
        "exception_repr": repr(exc),
        "traceback": traceback.format_exception(type(exc), exc, exc.__traceback__),
        "cwd": os.getcwd(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "pythonpath": os.environ.get("PYTHONPATH"),
        "sc2path": os.environ.get("SC2PATH"),
        "sc2_executable": str(installation.executable),
        "map_name": request.map_name or request.map_id,
        "map_file": request.map_file,
        "resolved_map_path": map_path,
        "replay_path": str(replay_path),
        "output_dir": str(output_dir),
        "bot_config": request.bot_config,
        "bot_config_id": request.bot_config_id,
        "opponent_id": request.opponent_id,
        "opponent_race": request.opponent_race,
        "opponent_difficulty": request.opponent_difficulty,
    }
    _write_json(output_dir / "launch_error_diagnostics.json", diagnostics)


def _write_failure_result(
    output_dir: Path,
    match_id: str,
    bot_name: str,
    request: MatchRequest,
    reason: str,
    status: str,
    telemetry_path: str,
    replay_metadata_path: str,
    started_at: str | None = None,
) -> MatchResult:
    result = MatchResult(
        match_id=match_id,
        status=status,
        result="unknown",
        mode=request.launch_mode,
        bot_name=bot_name,
        map_id=request.map_id,
        opponent_id=request.opponent_id,
        telemetry_path=telemetry_path,
        replay_metadata_path=replay_metadata_path,
    )
    _write_json(
        output_dir / "match_result.json",
        {
            "match_id": result.match_id,
            "status": result.status,
            "result": result.result,
            "mode": result.mode,
            "bot_name": result.bot_name,
            "bot_config": request.bot_config,
            "bot_config_id": request.bot_config_id,
            "bot_config_tags": list(request.bot_config_tags),
            "opponent_model_mode": "unknown",
            "map_id": result.map_id,
            "opponent_id": result.opponent_id,
            "opponent_race": request.opponent_race,
            "opponent_difficulty": request.opponent_difficulty,
            "opponent_tags": list(request.opponent_tags),
            "telemetry_path": result.telemetry_path,
            "replay_metadata_path": result.replay_metadata_path,
            "failure_reason": reason,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": _duration_seconds(started_at),
            "replay_path": None,
        },
    )
    return result


def _duration_seconds(started_at: str | None) -> float | None:
    if not started_at:
        return None
    started = datetime.fromisoformat(started_at)
    return (datetime.now(timezone.utc) - started).total_seconds()


def _status_from_exit_reason(exit_reason: str | None) -> str:
    if exit_reason in {"max_steps_reached", "max_game_time_reached", "gameplay_error"}:
        return exit_reason
    return "completed"


def run_local_dry_match(request: MatchRequest) -> MatchResult:
    match_id = f"dryrun-{uuid.uuid4().hex[:8]}"
    started_at = datetime.now(timezone.utc).isoformat()
    output_dir = Path(request.output_dir) / match_id
    telemetry_dir = output_dir / "telemetry"
    result_path = output_dir / "match_result.json"
    replay_metadata_path = output_dir / "replay_metadata.json"

    app = _build_bot_app(request, telemetry_dir)
    app.initialize()
    app.run()

    replay_metadata = {
        "match_id": match_id,
        "available": False,
        "replay_path": None,
        "reason": "local dry-run evaluation does not launch a real SC2 match yet",
        "map_id": request.map_id,
        "opponent_id": request.opponent_id,
    }
    _write_json(replay_metadata_path, replay_metadata)

    result = MatchResult(
        match_id=match_id,
        status="completed",
        result="unknown",
        mode="local_dry_run",
        bot_name=app.config.bot.name,
        map_id=request.map_id,
        opponent_id=request.opponent_id,
        telemetry_path=str(telemetry_dir / "events.jsonl"),
        replay_metadata_path=str(replay_metadata_path),
    )
    _write_json(
        result_path,
        {
            "match_id": result.match_id,
            "status": result.status,
            "result": result.result,
            "mode": result.mode,
            "bot_name": result.bot_name,
            "bot_config": request.bot_config,
            "bot_config_id": request.bot_config_id,
            "bot_config_tags": list(request.bot_config_tags),
            "opponent_model_mode": app.config.opponent_model.mode,
            "map_id": result.map_id,
            "opponent_id": result.opponent_id,
            "opponent_race": request.opponent_race,
            "opponent_difficulty": request.opponent_difficulty,
            "opponent_tags": list(request.opponent_tags),
            "telemetry_path": result.telemetry_path,
            "replay_metadata_path": result.replay_metadata_path,
            "replay_path": None,
            "failure_reason": None,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": _duration_seconds(started_at),
        },
    )
    return result


def run_real_launch_match(request: MatchRequest) -> MatchResult:
    match_id = f"reallaunch-{uuid.uuid4().hex[:8]}"
    started_at = datetime.now(timezone.utc).isoformat()
    output_dir = Path(request.output_dir) / match_id
    telemetry_dir = output_dir / "telemetry"
    preflight_path = output_dir / "preflight.json"
    replay_metadata_path = output_dir / "replay_metadata.json"
    replay_file = output_dir / "match.SC2Replay"
    app = _build_bot_app(request, telemetry_dir)
    preflight = run_sc2_preflight()
    _write_json(preflight_path, preflight.to_dict())
    _write_json(
        replay_metadata_path,
        {
            "match_id": match_id,
            "available": False,
            "replay_path": str(replay_file),
            "reason": "real local match replay will be written if launch succeeds",
            "map_id": request.map_id,
            "opponent_id": request.opponent_id,
        },
    )

    if not preflight.ok:
        return _write_failure_result(
            output_dir=output_dir,
            match_id=match_id,
            bot_name=app.config.bot.name,
            request=request,
            reason=preflight.message,
            status="launch_error",
            telemetry_path=str(telemetry_dir / "events.jsonl"),
            replay_metadata_path=str(replay_metadata_path),
            started_at=started_at,
        )

    try:
        installation = resolve_sc2_installation_from_env()
    except SC2InstallationError as exc:
        return _write_failure_result(
            output_dir=output_dir,
            match_id=match_id,
            bot_name=app.config.bot.name,
            request=request,
            reason=str(exc),
            status="config_error",
            telemetry_path=str(telemetry_dir / "events.jsonl"),
            replay_metadata_path=str(replay_metadata_path),
            started_at=started_at,
        )

    app.initialize()
    try:
        result_name = _run_python_sc2_local_game(request, app, installation, replay_file)
    except SC2InstallationError as exc:
        return _write_failure_result(
            output_dir=output_dir,
            match_id=match_id,
            bot_name=app.config.bot.name,
            request=request,
            reason=str(exc),
            status="config_error",
            telemetry_path=str(telemetry_dir / "events.jsonl"),
            replay_metadata_path=str(replay_metadata_path),
            started_at=started_at,
        )
    except Exception as exc:
        _write_launch_error_diagnostics(output_dir, exc, request, installation, replay_file)
        return _write_failure_result(
            output_dir=output_dir,
            match_id=match_id,
            bot_name=app.config.bot.name,
            request=request,
            reason=f"Real local match launch failed: {exc}",
            status="launch_error",
            telemetry_path=str(telemetry_dir / "events.jsonl"),
            replay_metadata_path=str(replay_metadata_path),
            started_at=started_at,
        )

    status = _status_from_exit_reason(app.container.runtime_exit_reason)
    result = MatchResult(
        match_id=match_id,
        status=status,
        result=result_name,
        mode="real_launch",
        bot_name=app.config.bot.name,
        map_id=request.map_id,
        opponent_id=request.opponent_id,
        telemetry_path=str(telemetry_dir / "events.jsonl"),
        replay_metadata_path=str(replay_metadata_path),
    )
    _write_json(
        output_dir / "match_result.json",
        {
            "match_id": result.match_id,
            "status": result.status,
            "result": result.result,
            "mode": result.mode,
            "bot_name": result.bot_name,
            "bot_config": request.bot_config,
            "bot_config_id": request.bot_config_id,
            "bot_config_tags": list(request.bot_config_tags),
            "opponent_model_mode": app.config.opponent_model.mode,
            "map_id": result.map_id,
            "opponent_id": result.opponent_id,
            "opponent_race": request.opponent_race,
            "opponent_difficulty": request.opponent_difficulty,
            "opponent_tags": list(request.opponent_tags),
            "telemetry_path": result.telemetry_path,
            "replay_metadata_path": result.replay_metadata_path,
            "replay_path": str(replay_file),
            "failure_reason": None,
            "exit_reason": app.container.runtime_exit_reason,
            "started_at": started_at,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": _duration_seconds(started_at),
            "launch_message": "Real local match completed through python-sc2.",
            "runtime_max_game_loop": app.config.runtime.max_game_loop,
            "requested_game_time_limit_seconds": _game_time_limit_seconds(app.config.runtime),
        },
    )
    _write_json(
        replay_metadata_path,
        {
            "match_id": match_id,
            "available": replay_file.exists(),
            "replay_path": str(replay_file),
            "reason": None,
            "map_id": request.map_id,
            "opponent_id": request.opponent_id,
        },
    )
    return result


def run_match(request: MatchRequest) -> dict[str, str]:
    if request.launch_mode == "real_launch":
        result = run_real_launch_match(request)
    else:
        result = run_local_dry_match(request)
    return {
        "status": result.status,
        "mode": result.mode,
        "match_id": result.match_id,
        "bot_config": request.bot_config,
        "bot_config_id": request.bot_config_id,
        "map_id": result.map_id,
        "opponent_id": result.opponent_id,
    }
