"""Tiny JSONL telemetry logger."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sc2bot.telemetry.schema import TelemetryEvent


class EventLogger:
    def __init__(self, output_dir: str | Path, enabled: bool = True) -> None:
        self.output_dir = Path(output_dir)
        self.enabled = enabled
        self.file_name = "events.jsonl"

    @property
    def path(self) -> Path:
        return self.output_dir / self.file_name

    def record(self, event_type: str, payload: dict[str, Any] | None = None) -> None:
        if not self.enabled:
            return
        self.output_dir.mkdir(parents=True, exist_ok=True)
        event = TelemetryEvent(event_type=event_type, payload=payload or {})
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
