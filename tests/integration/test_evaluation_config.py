from pathlib import Path

import json

from evaluation.runner.collect_results import collect_results
from evaluation.runner.run_batch import _bot_config_entries, load_batch_config
from evaluation.runner.run_match import MatchRequest, _game_time_limit_seconds, run_local_dry_match, run_match
from sc2bot.config.loader import load_bot_config


def test_smoke_evaluation_config_loads():
    config = load_batch_config(Path("configs/evaluation/smoke.yaml"))

    assert config["evaluation"]["name"] == "smoke"
    assert config["evaluation"]["repeats"] == 1
    entries = _bot_config_entries(config["evaluation"])
    assert entries == [
        {
            "id": "default",
            "path": "configs/bot/debug.yaml",
            "tags": (),
            "run_class": "unspecified",
            "validation_class": "unspecified",
        }
    ]


def test_phase1d_ablation_config_loads_multiple_bot_configs():
    config = load_batch_config(Path("configs/evaluation/phase1d_ablation_opponent_model.yaml"))

    entries = _bot_config_entries(config["evaluation"])

    assert [item["id"] for item in entries] == ["null", "rule_based"]
    assert entries[0]["path"] == "configs/bot/opponent_model_null.yaml"


def test_phase_a_smoke_config_is_four_match_shape():
    from evaluation.runner.run_batch import _enabled_entries

    config = load_batch_config(Path("configs/evaluation/phase_a_real_smoke.yaml"))
    evaluation = config["evaluation"]
    maps = _enabled_entries(evaluation["maps_config"], "maps")
    opponents = _enabled_entries(evaluation["opponents_config"], "opponents")

    assert evaluation["launch_mode"] == "real_launch"
    assert evaluation["repeats"] == 2
    assert len(maps) == 1
    assert len(opponents) == 2
    assert len(maps) * len(opponents) * evaluation["repeats"] == 4


def test_phase_a_baseline_chunk_1_config_is_eight_match_shape():
    from evaluation.runner.run_batch import _enabled_entries

    config = load_batch_config(Path("configs/evaluation/phase_a_baseline_v0_chunk_1.yaml"))
    evaluation = config["evaluation"]
    maps = _enabled_entries(evaluation["maps_config"], "maps")
    opponents = _enabled_entries(evaluation["opponents_config"], "opponents")

    assert evaluation["launch_mode"] == "real_launch"
    assert evaluation["repeats"] == 2
    assert evaluation["run_id"] == "phase_a_baseline_v0_chunk_1"
    assert len(maps) == 1
    assert len(opponents) == 4
    assert {opponent["race"] for opponent in opponents} == {"terran", "zerg"}
    assert {opponent["difficulty"] for opponent in opponents} == {"easy", "medium"}
    assert len(maps) * len(opponents) * evaluation["repeats"] == 8


def test_phase_a_baseline_chunk_2_configs_are_combined_eight_match_shape():
    from evaluation.runner.run_batch import _enabled_entries

    total = 0
    coverage = set()
    for config_path in (
        "configs/evaluation/phase_a_baseline_v0_chunk_2a.yaml",
        "configs/evaluation/phase_a_baseline_v0_chunk_2b.yaml",
    ):
        config = load_batch_config(Path(config_path))
        evaluation = config["evaluation"]
        maps = _enabled_entries(evaluation["maps_config"], "maps")
        opponents = _enabled_entries(evaluation["opponents_config"], "opponents")
        total += len(maps) * len(opponents) * evaluation["repeats"]
        for map_item in maps:
            for opponent in opponents:
                coverage.add((map_item["id"], opponent["race"], opponent["difficulty"]))

    assert total == 8
    assert coverage == {
        ("incorporeal_aie_v4", "protoss", "easy"),
        ("incorporeal_aie_v4", "protoss", "medium"),
        ("leylines_aie_v3", "terran", "easy"),
        ("leylines_aie_v3", "terran", "medium"),
    }


def test_phase_a_baseline_chunk_3_config_is_eight_match_shape():
    from evaluation.runner.run_batch import _enabled_entries

    config = load_batch_config(Path("configs/evaluation/phase_a_baseline_v0_chunk_3.yaml"))
    evaluation = config["evaluation"]
    maps = _enabled_entries(evaluation["maps_config"], "maps")
    opponents = _enabled_entries(evaluation["opponents_config"], "opponents")

    assert evaluation["launch_mode"] == "real_launch"
    assert evaluation["repeats"] == 2
    assert evaluation["run_id"] == "phase_a_baseline_v0_chunk_3"
    assert [item["id"] for item in maps] == ["leylines_aie_v3"]
    assert len(opponents) == 4
    assert {opponent["race"] for opponent in opponents} == {"zerg", "protoss"}
    assert {opponent["difficulty"] for opponent in opponents} == {"easy", "medium"}
    assert len(maps) * len(opponents) * evaluation["repeats"] == 8


def test_phase_b_revalidation_duration_probe_config_uses_gameplay_runtime_window():
    from evaluation.runner.run_batch import _enabled_entries

    config = load_batch_config(Path("configs/evaluation/phase_b_revalidation_duration_probe.yaml"))
    evaluation = config["evaluation"]
    maps = _enabled_entries(evaluation["maps_config"], "maps")
    opponents = _enabled_entries(evaluation["opponents_config"], "opponents")
    bot_config = load_bot_config(evaluation["bot_config"])

    assert evaluation["launch_mode"] == "real_launch"
    assert evaluation["bot_config"] == "configs/bot/baseline_playable.yaml"
    assert evaluation["bot_config"] != "configs/bot/debug.yaml"
    assert evaluation["run_class"] == "baseline_playable"
    assert evaluation["validation_class"] == "gameplay_capability"
    assert evaluation["repeats"] == 1
    assert len(maps) == 1
    assert len(opponents) >= 1
    assert bot_config.runtime.max_game_loop >= 9600
    assert _game_time_limit_seconds(bot_config.runtime) >= 400


def test_run_game_time_limit_derives_from_runtime_max_game_loop():
    debug_config = load_bot_config(Path("configs/bot/debug.yaml"))
    gameplay_config = load_bot_config(Path("configs/bot/phase_b_revalidation_gameplay.yaml"))

    assert _game_time_limit_seconds(debug_config.runtime) < 180
    assert _game_time_limit_seconds(gameplay_config.runtime) >= 300


def test_local_dry_match_persists_result(tmp_path):
    result = run_local_dry_match(
        MatchRequest(
            bot_config="configs/bot/debug.yaml",
            bot_config_id="debug",
            map_id="incorporeal_aie_v4",
            map_name="IncorporealAIE_v4",
            map_file="IncorporealAIE_v4.SC2Map",
            opponent_id="builtin_easy_terran",
            output_dir=str(tmp_path),
        )
    )

    assert result.status == "completed"
    assert Path(result.telemetry_path).exists()
    results = collect_results(tmp_path)
    assert len(results) == 1


def test_run_match_real_launch_failure_persists_reason(tmp_path, monkeypatch):
    monkeypatch.delenv("SC2PATH", raising=False)

    result = run_match(
        MatchRequest(
            bot_config="configs/bot/debug.yaml",
            bot_config_id="debug",
            map_id="incorporeal_aie_v4",
            map_name="IncorporealAIE_v4",
            map_file="IncorporealAIE_v4.SC2Map",
            opponent_id="builtin_easy_terran",
            output_dir=str(tmp_path),
            launch_mode="real_launch",
        )
    )

    assert result["status"] == "launch_error"
    match_dir = next(tmp_path.glob("reallaunch-*"))
    payload = json.loads((match_dir / "match_result.json").read_text(encoding="utf-8"))
    assert "SC2PATH is not set" in payload["failure_reason"]
    assert (match_dir / "preflight.json").exists()


def test_run_match_real_launch_uses_real_game_path(tmp_path, monkeypatch):
    from evaluation.runner import run_match as run_match_module
    from sc2bot.runtime.sc2_installation import SC2Installation, SC2PreflightResult

    install_root = tmp_path / "StarCraft II"
    (install_root / "Maps").mkdir(parents=True)
    (install_root / "Maps" / "IncorporealAIE_v4.SC2Map").write_text("stub", encoding="utf-8")
    (install_root / "Versions").mkdir()
    (install_root / "Support64").mkdir()
    (install_root / "SC2Data").mkdir()
    (install_root / "StarCraft II.exe").write_text("stub", encoding="utf-8")

    installation = SC2Installation(
        root=install_root,
        versions_dir=install_root / "Versions",
        support64_dir=install_root / "Support64",
        sc2data_dir=install_root / "SC2Data",
        executable=install_root / "StarCraft II.exe",
    )

    monkeypatch.setattr(
        run_match_module,
        "run_sc2_preflight",
        lambda: SC2PreflightResult(
            ok=True,
            sc2path=str(install_root),
            executable=str(installation.executable),
            python_version="3.11.5",
            message="ok",
        ),
    )
    monkeypatch.setattr(
        run_match_module,
        "resolve_sc2_installation_from_env",
        lambda: installation,
    )
    monkeypatch.setattr(
        run_match_module,
        "_run_python_sc2_local_game",
        lambda request, app, installation, replay_path: "Result.Defeat",
    )

    result = run_match(
        MatchRequest(
            bot_config="configs/bot/debug.yaml",
            bot_config_id="debug",
            map_id="incorporeal_aie_v4",
            map_name="IncorporealAIE_v4",
            map_file="IncorporealAIE_v4.SC2Map",
            opponent_id="builtin_easy_terran",
            output_dir=str(tmp_path),
            launch_mode="real_launch",
        )
    )

    assert result["status"] == "completed"
    match_dir = next(tmp_path.glob("reallaunch-*"))
    payload = json.loads((match_dir / "match_result.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "real_launch"
    assert payload["result"] == "Result.Defeat"
    assert payload["bot_config_id"] == "debug"
    assert payload["runtime_max_game_loop"] == 2600
    assert payload["requested_game_time_limit_seconds"] == _game_time_limit_seconds(
        load_bot_config(Path("configs/bot/debug.yaml")).runtime
    )


def test_run_match_real_launch_bot_opponent_persists_metadata(tmp_path, monkeypatch):
    from evaluation.runner import run_match as run_match_module
    from sc2bot.runtime.sc2_installation import SC2Installation, SC2PreflightResult

    install_root = tmp_path / "StarCraft II"
    (install_root / "Maps").mkdir(parents=True)
    (install_root / "Maps" / "IncorporealAIE_v4.SC2Map").write_text("stub", encoding="utf-8")
    (install_root / "Versions").mkdir()
    (install_root / "Support64").mkdir()
    (install_root / "SC2Data").mkdir()
    (install_root / "StarCraft II.exe").write_text("stub", encoding="utf-8")

    installation = SC2Installation(
        root=install_root,
        versions_dir=install_root / "Versions",
        support64_dir=install_root / "Support64",
        sc2data_dir=install_root / "SC2Data",
        executable=install_root / "StarCraft II.exe",
    )

    monkeypatch.setattr(
        run_match_module,
        "run_sc2_preflight",
        lambda: SC2PreflightResult(
            ok=True,
            sc2path=str(install_root),
            executable=str(installation.executable),
            python_version="3.11.5",
            message="ok",
        ),
    )
    monkeypatch.setattr(
        run_match_module,
        "resolve_sc2_installation_from_env",
        lambda: installation,
    )
    monkeypatch.setattr(
        run_match_module,
        "_run_python_sc2_local_game",
        lambda request, app, installation, replay_path: "Result.Victory",
    )

    result = run_match(
        MatchRequest(
            bot_config="configs/bot/debug.yaml",
            bot_config_id="debug",
            map_id="incorporeal_aie_v4",
            map_name="IncorporealAIE_v4",
            map_file="IncorporealAIE_v4.SC2Map",
            opponent_id="external_frozen_r5_comparator",
            opponent_type="bot",
            opponent_bot_config="configs/bot/adaptive_research.yaml",
            opponent_bot_config_id="frozen_r5_comparator_house_bot",
            opponent_bot_config_tags=("external", "house_bot"),
            output_dir=str(tmp_path),
            launch_mode="real_launch",
        )
    )

    assert result["status"] == "completed"
    assert result["opponent_type"] == "bot"
    match_dir = next(tmp_path.glob("reallaunch-*"))
    payload = json.loads((match_dir / "match_result.json").read_text(encoding="utf-8"))
    assert payload["opponent_type"] == "bot"
    assert payload["opponent_bot_config"] == "configs/bot/adaptive_research.yaml"
    assert payload["opponent_bot_config_id"] == "frozen_r5_comparator_house_bot"
    assert payload["opponent_bot_config_tags"] == ["external", "house_bot"]


def test_run_match_real_launch_missing_map_persists_reason(tmp_path, monkeypatch):
    from evaluation.runner import run_match as run_match_module
    from sc2bot.runtime.sc2_installation import SC2Installation, SC2PreflightResult

    install_root = tmp_path / "StarCraft II"
    (install_root / "Maps").mkdir(parents=True)
    (install_root / "Versions").mkdir()
    (install_root / "Support64").mkdir()
    (install_root / "SC2Data").mkdir()
    (install_root / "StarCraft II.exe").write_text("stub", encoding="utf-8")

    installation = SC2Installation(
        root=install_root,
        versions_dir=install_root / "Versions",
        support64_dir=install_root / "Support64",
        sc2data_dir=install_root / "SC2Data",
        executable=install_root / "StarCraft II.exe",
    )

    monkeypatch.setattr(
        run_match_module,
        "run_sc2_preflight",
        lambda: SC2PreflightResult(
            ok=True,
            sc2path=str(install_root),
            executable=str(installation.executable),
            python_version="3.11.5",
            message="ok",
        ),
    )
    monkeypatch.setattr(
        run_match_module,
        "resolve_sc2_installation_from_env",
        lambda: installation,
    )

    result = run_match(
        MatchRequest(
            bot_config="configs/bot/debug.yaml",
            map_id="incorporeal_aie_v4",
            map_name="IncorporealAIE_v4",
            map_file="IncorporealAIE_v4.SC2Map",
            opponent_id="builtin_easy_terran",
            output_dir=str(tmp_path),
            launch_mode="real_launch",
        )
    )

    assert result["status"] == "config_error"
    match_dir = next(tmp_path.glob("reallaunch-*"))
    payload = json.loads((match_dir / "match_result.json").read_text(encoding="utf-8"))
    assert "Configured map file does not exist" in payload["failure_reason"]


def test_local_opponent_pool_contains_multiple_enabled_opponents():
    from evaluation.runner.run_batch import _enabled_entries

    opponents = _enabled_entries("configs/opponents/local_pool.yaml", "opponents")

    assert len(opponents) >= 4
    assert all("tags" in opponent for opponent in opponents)
