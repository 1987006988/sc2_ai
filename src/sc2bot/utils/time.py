"""Time helpers."""


def game_loop_to_seconds(game_loop: int, loops_per_second: float = 22.4) -> float:
    return game_loop / loops_per_second
