import pytest

from evaluation.runner.build_collection_config import build_collection_config


def _levels_payload():
    return {
        "collection_levels": {
            "smoke": {
                "maps_config": "configs/maps/phase_a_smoke_maps.yaml",
                "opponents_config": "configs/opponents/phase_a_smoke_pool.yaml",
                "repeats": 2,
                "output_dir": "data/logs/evaluation/smoke",
            },
            "evaluation": {
                "maps_config": "configs/maps/local_test_maps.yaml",
                "opponents_config": "configs/opponents/phase_a_builtin_easy_medium_pool.yaml",
                "repeats": 5,
                "output_dir": "data/logs/evaluation/evaluation",
            },
        },
        "defaults": {
            "bot_config": "configs/bot/debug.yaml",
            "launch_mode": "dry_run",
            "isolate_runs": True,
            "fail_on_crash": False,
            "include_historical_by_default": False,
            "large_real_match_threshold": 50,
        },
    }


def test_build_collection_config_defaults_to_dry_scoped_run():
    config = build_collection_config(
        _levels_payload(),
        level_id="smoke",
        run_id="run_1",
    )

    evaluation = config["evaluation"]
    assert evaluation["launch_mode"] == "dry_run"
    assert evaluation["run_id"] == "run_1"
    assert evaluation["isolate_runs"] is True
    assert evaluation["include_historical_by_default"] is False
    assert evaluation["expected_match_count"] == 4


def test_build_collection_config_blocks_large_real_run_without_ack():
    with pytest.raises(ValueError, match="large real collection requires"):
        build_collection_config(
            _levels_payload(),
            level_id="evaluation",
            run_id="eval_1",
            launch_mode="real_launch",
        )


def test_build_collection_config_allows_large_real_run_with_ack():
    config = build_collection_config(
        _levels_payload(),
        level_id="evaluation",
        run_id="eval_1",
        launch_mode="real_launch",
        allow_large_real=True,
    )

    assert config["evaluation"]["launch_mode"] == "real_launch"
    assert config["evaluation"]["expected_match_count"] == 60


def test_build_collection_config_supports_repeat_override():
    config = build_collection_config(
        _levels_payload(),
        level_id="evaluation",
        run_id="regression_like",
        repeats=1,
    )

    assert config["evaluation"]["expected_match_count"] == 12
