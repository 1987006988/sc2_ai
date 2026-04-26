from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sc2reader


OBSERVATION_WINDOW_SECONDS = 90
DECISION_WINDOW_SECONDS = 180
FUTURE_WINDOW_SECONDS = 300
FRAME_BUCKETS = (30, 60, 90)
CANDIDATE_ACTION_SLATE = (
    "expand_now",
    "add_production",
    "add_tech",
    "add_upgrade",
    "increase_production_tempo",
    "defensive_hold",
    "move_out_window_open",
    "delay_move_out",
)

EXPAND_ABILITIES = {"BuildNexus", "BuildCommandCenter", "BuildHatchery"}
PRODUCTION_ABILITIES = {
    "BuildGateway",
    "BuildBarracks",
    "BuildFactory",
    "BuildStarport",
    "BuildSpawningPool",
    "BuildRoachWarren",
    "BuildRoboticsFacility",
    "BuildStargate",
    "BuildWarpGate",
}
TECH_ABILITIES = {
    "BuildCyberneticsCore",
    "BuildForge",
    "BuildEvolutionChamber",
    "BuildBanelingNest",
    "BuildSpire",
    "BuildHydraliskDen",
    "BuildTwilightCouncil",
    "BuildTemplarArchive",
    "BuildDarkShrine",
    "BuildFleetBeacon",
    "BuildFusionCore",
    "BuildEngineeringBay",
    "BuildArmory",
}
DETECTION_ABILITIES = {
    "BuildPhotonCannon",
    "BuildMissileTurret",
    "BuildSporeCrawler",
    "BuildSpineCrawler",
    "BuildBunker",
    "BuildShieldBattery",
    "TrainObserver",
}
WORKER_ECON_ABILITIES = {
    "TrainSCV",
    "TrainProbe",
    "TrainDrone",
    "MorphDrone",
    "MorphOverlord",
}
COMBAT_ACTION_PREFIXES = ("Train", "WarpIn", "Morph")
UPGRADE_PREFIXES = ("Research", "Upgrade")


@dataclass(frozen=True)
class ParsedReplaySample:
    replay_id: str
    player_pid: int
    sample: dict[str, Any]


def canonical_race_name(race: str) -> str:
    value = str(race).strip().lower()
    mapping = {
        "терраны": "Terran",
        "протоссы": "Protoss",
        "зерги": "Zerg",
        "terran": "Terran",
        "protoss": "Protoss",
        "zerg": "Zerg",
        "random": "Random",
    }
    return mapping.get(value, str(race))


def _categorize_ability(ability_name: str) -> str:
    if ability_name in EXPAND_ABILITIES:
        return "expand"
    if ability_name in DETECTION_ABILITIES:
        return "defense"
    if ability_name in PRODUCTION_ABILITIES:
        return "production"
    if ability_name in TECH_ABILITIES:
        return "tech"
    if ability_name.startswith(UPGRADE_PREFIXES):
        return "upgrade"
    if ability_name == "Attack":
        return "attack"
    if ability_name in WORKER_ECON_ABILITIES:
        return "worker_econ"
    if ability_name.startswith(COMBAT_ACTION_PREFIXES):
        return "combat_unit"
    return "other"


def _bucket_game_length(seconds: int) -> str:
    if seconds < 240:
        return "short"
    if seconds < 480:
        return "medium"
    return "long"


def _production_tempo_bucket(combat_unit_count: int) -> str:
    if combat_unit_count >= 10:
        return "high"
    if combat_unit_count >= 4:
        return "medium"
    return "low"


def _opening_label(counter: Counter[str]) -> str:
    if counter["expand"] > 0:
        return "fast_expand"
    if counter["tech"] > 0:
        return "tech_open"
    if counter["production"] > 0 or counter["combat_unit"] >= 2:
        return "pressure_open"
    return "econ_open"


def _tech_path_label(counter: Counter[str]) -> str:
    if counter["tech"] > 0:
        return "tech_path_present"
    if counter["upgrade"] > 0:
        return "upgrade_path"
    if counter["production"] > 1:
        return "production_path"
    return "low_tech"


def _macro_action_label(counter: Counter[str], attack_count: int) -> str:
    if counter["expand"] > 0:
        return "expand_now"
    if counter["defense"] > 0:
        return "defensive_hold"
    if counter["tech"] > 0:
        return "add_tech"
    if counter["production"] > 0:
        return "add_production"
    if counter["upgrade"] > 0:
        return "add_upgrade"
    if attack_count >= 3:
        return "move_out_window_open"
    if counter["combat_unit"] >= 4:
        return "increase_production_tempo"
    return "delay_move_out"


def _future_pressure_label(counter: Counter[str], attack_count: int) -> str:
    return "high_pressure" if attack_count >= 3 or counter["combat_unit"] >= 4 else "low_pressure"


def _participant_events(replay: Any) -> dict[int, list[dict[str, Any]]]:
    events_by_pid: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in replay.events:
        ability_name = getattr(event, "ability_name", None)
        player = getattr(event, "player", None)
        if not ability_name or player is None or getattr(player, "pid", None) not in (1, 2):
            continue
        events_by_pid[player.pid].append(
            {
                "second": int(getattr(event, "second", 0)),
                "ability_name": str(ability_name),
                "category": _categorize_ability(str(ability_name)),
            }
        )
    return events_by_pid


def _window_counter(events: list[dict[str, Any]], start_second: int, end_second: int) -> tuple[Counter[str], int]:
    counter: Counter[str] = Counter()
    attack_count = 0
    for event in events:
        second = int(event["second"])
        if start_second < second <= end_second:
            category = str(event["category"])
            counter[category] += 1
            if category == "attack":
                attack_count += 1
    return counter, attack_count


def _frames(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    for bucket in FRAME_BUCKETS:
        counter, attack_count = _window_counter(events, 0, bucket)
        frames.append(
            {
                "game_time": float(bucket),
                "expand_count": counter["expand"],
                "production_count": counter["production"],
                "tech_count": counter["tech"],
                "upgrade_count": counter["upgrade"],
                "defense_count": counter["defense"],
                "combat_unit_count": counter["combat_unit"],
                "worker_econ_count": counter["worker_econ"],
                "attack_count": attack_count,
            }
        )
    return frames


def parse_replay_to_samples(replay_path: Path) -> list[ParsedReplaySample]:
    replay = sc2reader.load_replay(str(replay_path), load_level=4)
    events_by_pid = _participant_events(replay)
    samples: list[ParsedReplaySample] = []

    for player in replay.players:
        pid = int(player.pid)
        own_events = events_by_pid.get(pid, [])
        if not own_events:
            continue
        enemy = next(candidate for candidate in replay.players if candidate.pid != pid)
        enemy_events = events_by_pid.get(int(enemy.pid), [])

        own_obs_counter, own_obs_attacks = _window_counter(own_events, 0, OBSERVATION_WINDOW_SECONDS)
        own_decision_counter, own_decision_attacks = _window_counter(
            own_events, OBSERVATION_WINDOW_SECONDS, DECISION_WINDOW_SECONDS
        )
        own_future_counter, own_future_attacks = _window_counter(
            own_events, DECISION_WINDOW_SECONDS, FUTURE_WINDOW_SECONDS
        )
        enemy_obs_counter, _ = _window_counter(enemy_events, 0, OBSERVATION_WINDOW_SECONDS)
        enemy_full_early_counter, _ = _window_counter(enemy_events, 0, DECISION_WINDOW_SECONDS)

        result = str(player.result).lower()
        winner = "win" if result == "win" else "loss"

        sample = {
            "sample_id": f"{replay_path.stem}_p{pid}",
            "source_id": "distar_zvz_agent_platform",
            "replay_id": replay_path.name,
            "replay_series_id": replay_path.stem,
            "game_time": float(OBSERVATION_WINDOW_SECONDS),
            "map": replay.map_name,
            "matchup": f"{canonical_race_name(player.play_race)}v{canonical_race_name(enemy.play_race)}",
            "time_window_bucket": "obs_0_90_decision_90_180_future_180_300",
            "player_identity": {
                "pid": pid,
                "race": canonical_race_name(player.play_race),
                "result": winner,
            },
            "own_visible_state": {
                "own_race": canonical_race_name(player.play_race),
                "expand_count": own_obs_counter["expand"],
                "production_count": own_obs_counter["production"],
                "tech_count": own_obs_counter["tech"],
                "upgrade_count": own_obs_counter["upgrade"],
                "defense_count": own_obs_counter["defense"],
                "combat_unit_count": own_obs_counter["combat_unit"],
                "worker_econ_count": own_obs_counter["worker_econ"],
                "attack_count": own_obs_attacks,
            },
            "observed_enemy_state": {
                "enemy_race": canonical_race_name(enemy.play_race),
                "enemy_commands_visible_count": 0,
                "enemy_visibility_mode": "teacher_proxy_hidden",
            },
            "hidden_enemy_label": {
                "opening_class": _opening_label(enemy_obs_counter),
                "tech_path": _tech_path_label(enemy_full_early_counter),
            },
            "enemy_opening_class": _opening_label(enemy_obs_counter),
            "enemy_tech_path": _tech_path_label(enemy_full_early_counter),
            "macro_action_label": _macro_action_label(own_decision_counter, own_decision_attacks),
            "production_tempo_label": _production_tempo_bucket(own_decision_counter["combat_unit"]),
            "candidate_action_slate": list(CANDIDATE_ACTION_SLATE),
            "future_outcome_label": {
                "winner": winner,
                "game_length_bucket": _bucket_game_length(replay.game_length.seconds),
                "future_pressure_proxy": _future_pressure_label(own_future_counter, own_future_attacks),
            },
            "future_winner": winner,
            "future_game_length_bucket": _bucket_game_length(replay.game_length.seconds),
            "future_pressure_proxy": _future_pressure_label(own_future_counter, own_future_attacks),
            "winner": winner,
            "frames": _frames(own_events),
            "provenance": {
                "source_type": "acquired_strong_bot_replay_corpus",
                "source_commit": "12b1c69350ad41e17895c602a66a52d98dd58452",
                "replay_path": str(replay_path),
            },
        }
        samples.append(ParsedReplaySample(replay_id=replay_path.name, player_pid=pid, sample=sample))
    return samples
