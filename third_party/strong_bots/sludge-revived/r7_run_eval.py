"""Run one sludge-revived R7 evaluation match and emit auditable artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sc2 import AIBuild, Difficulty, Race, maps, run_game
from sc2.player import Bot, Computer

from bot.r7.bots import R7BaselineBot, R7RuleAdvisorBot, R7WorldAdvisorBot
from bot.r7.runtime_state import configure


def _difficulty(name: str) -> Difficulty:
    return getattr(Difficulty, name.capitalize())


def _race(name: str) -> Race:
    return getattr(Race, name.capitalize())


def _build(name: str) -> AIBuild:
    return getattr(AIBuild, name)


def _example_opponent(name: str) -> tuple[Race, object]:
    key = name.strip().lower()
    if key == "worker_rush":
        from examples.worker_rush import WorkerRushBot

        return Race.Zerg, WorkerRushBot()
    if key == "zerg_rush":
        from examples.zerg.zerg_rush import ZergRushBot

        return Race.Zerg, ZergRushBot()
    if key == "hydralisk_push":
        from examples.zerg.hydralisk_push import Hydralisk

        return Race.Zerg, Hydralisk()
    if key == "warpgate_push":
        from examples.protoss.warpgate_push import WarpGateBot

        return Race.Protoss, WarpGateBot()
    raise ValueError(f"Unsupported example external opponent: {name}")


def _normalize_result(result: object) -> str:
    if isinstance(result, (list, tuple)) and result:
        return str(result[0])
    return str(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", choices=("baseline", "rule", "world"), required=True)
    parser.add_argument("--map", default="KairosJunctionLE")
    parser.add_argument("--opponent-race", default="Terran")
    parser.add_argument("--difficulty", default="Medium")
    parser.add_argument("--ai-build", default="Timing")
    parser.add_argument("--opponent-kind", choices=("computer", "example_bot"), default="computer")
    parser.add_argument("--opponent-bot", default="")
    parser.add_argument("--game-time-limit", type=int, default=420)
    parser.add_argument("--step-time-limit", type=float, default=2.0)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--world-model-path", default="")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    replay_path = output_dir / "match.SC2Replay"
    telemetry_path = output_dir / "advisor_stats.json"
    result_path = output_dir / "match_result.json"

    configure(arm=args.arm, world_model_path=args.world_model_path)

    if args.arm == "baseline":
        ai = R7BaselineBot(str(telemetry_path))
    elif args.arm == "rule":
        ai = R7RuleAdvisorBot(str(telemetry_path))
    else:
        ai = R7WorldAdvisorBot(str(telemetry_path))

    players = [Bot(Race.Zerg, ai)]
    if args.opponent_kind == "computer":
        players.append(
            Computer(_race(args.opponent_race), _difficulty(args.difficulty), ai_build=_build(args.ai_build))
        )
    else:
        opponent_race, opponent_ai = _example_opponent(args.opponent_bot)
        players.append(Bot(opponent_race, opponent_ai))

    result = None
    run_error: dict[str, object] | None = None
    try:
        result = run_game(
            maps.get(args.map),
            players,
            realtime=False,
            step_time_limit=args.step_time_limit,
            game_time_limit=args.game_time_limit,
            save_replay_as=str(replay_path),
        )
        normalized_result = _normalize_result(result)
    except BaseException as exc:
        normalized_result = None
        run_error = {
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        if telemetry_path.exists():
            telemetry_payload = json.loads(telemetry_path.read_text(encoding="utf-8"))
            normalized_result = str(telemetry_payload.get("result") or "")
        if not normalized_result:
            raise
    payload = {
        "arm": args.arm,
        "map": args.map,
        "opponent_kind": args.opponent_kind,
        "opponent_bot": args.opponent_bot,
        "opponent_race": args.opponent_race,
        "difficulty": args.difficulty,
        "ai_build": args.ai_build,
        "game_time_limit": args.game_time_limit,
        "step_time_limit": args.step_time_limit,
        "result": normalized_result,
        "replay_path": str(replay_path),
        "telemetry_path": str(telemetry_path),
        "run_error": run_error,
    }
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
