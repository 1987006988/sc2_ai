"""Telemetry event schema definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = 1


@dataclass(frozen=True)
class TelemetryEvent:
    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    schema_version: int = SCHEMA_VERSION
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "created_at": self.created_at,
            "event_type": self.event_type,
            "payload": self.payload,
        }
