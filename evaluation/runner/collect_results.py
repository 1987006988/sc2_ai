"""Collect persisted batch results."""

from __future__ import annotations

import json
from pathlib import Path


def collect_results(output_dir: str | Path) -> list[dict]:
    root = Path(output_dir)
    if not root.exists():
        return []
    results: list[dict] = []
    for path in sorted(root.glob("*/match_result.json")):
        results.append(json.loads(path.read_text(encoding="utf-8")))
    return results
