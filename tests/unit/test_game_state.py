from sc2bot.domain.game_state import GameState
from sc2bot.runtime.game_loop import build_game_state_from_bot_ai


class _TypeId:
    def __init__(self, name: str) -> None:
        self.name = name


class _Unit:
    def __init__(self, name: str) -> None:
        self.type_id = _TypeId(name)


class _Position:
    x = 1.5
    y = 2.5


class _State:
    game_loop = 112


class _BotAI:
    state = _State()
    time = 5.0
    race = _TypeId("Protoss")
    enemy_race = _TypeId("Terran")
    start_location = _Position()
    enemy_start_locations = [_Position()]
    enemy_units = [_Unit("Marine")]
    enemy_structures = [_Unit("Barracks"), _Unit("CommandCenter")]
    workers = [_Unit("Probe")]
    army = [_Unit("Zealot")]
    townhalls = [_Unit("Nexus")]
    minerals = 50
    vespene = 0
    supply_used = 13
    supply_cap = 15


def test_game_state_to_dict_contains_live_fields():
    state = GameState(
        game_loop=10,
        game_time=1.0,
        own_race="protoss",
        visible_enemy_units=("marine",),
    )

    data = state.to_dict()

    assert data["game_loop"] == 10
    assert data["game_time"] == 1.0
    assert data["own_race"] == "protoss"
    assert data["visible_enemy_units"] == ["marine"]


def test_build_game_state_from_bot_ai_reads_live_snapshot():
    state = build_game_state_from_bot_ai(_BotAI())

    assert state.game_loop == 112
    assert state.game_time == 5.0
    assert state.own_race == "protoss"
    assert state.enemy_race == "terran"
    assert state.visible_enemy_units_count == 1
    assert state.visible_enemy_structures_count == 2
    assert state.visible_enemy_townhalls_count == 1
    assert state.own_workers_count == 1
    assert state.own_army_count == 1
