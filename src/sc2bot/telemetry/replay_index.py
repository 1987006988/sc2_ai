"""Replay index placeholder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReplayRecord:
    replay_path: Path
    match_id: str
    result: str | None = None


class ReplayIndex:
    def __init__(self) -> None:
        self.records: list[ReplayRecord] = []

    def add(self, record: ReplayRecord) -> None:
        self.records.append(record)
