from sc2bot.domain.game_state import GameState
from sc2bot.managers.scouting_manager import ScoutingManager


def test_scouting_manager_accumulates_live_enemy_observations():
    manager = ScoutingManager()

    observation = manager.update(
        GameState(
            game_loop=100,
            game_time=10.0,
            visible_enemy_units_count=1,
            visible_enemy_structures_count=1,
            visible_enemy_units=("zergling",),
            visible_enemy_structures=("spawningpool",),
        )
    )

    assert observation.first_enemy_seen_time == 10.0
    assert observation.last_enemy_seen_time == 10.0
    assert observation.seen_enemy_structures == ("spawningpool",)
    assert observation.seen_enemy_combat_units == ("zergling",)
    assert observation.possible_tech_signal is True
    assert observation.possible_rush_signal is True
    assert observation.observation_confidence > 0


def test_scouting_manager_preserves_last_seen_when_enemy_not_visible():
    manager = ScoutingManager()
    manager.update(
        GameState(
            game_loop=100,
            game_time=10.0,
            visible_enemy_units_count=1,
            visible_enemy_units=("marine",),
        )
    )

    observation = manager.update(GameState(game_loop=200, game_time=20.0))

    assert observation.first_enemy_seen_time == 10.0
    assert observation.last_enemy_seen_time == 10.0
    assert observation.enemy_units_seen == ("marine",)
