"""Strategy metric placeholders."""


def strategy_switch_count(events: list[dict]) -> int:
    return sum(1 for event in events if event.get("event_type") == "strategy_decision")
