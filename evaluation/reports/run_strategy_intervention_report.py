"""CLI wrapper for Phase 1E strategy-intervention reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from evaluation.metrics.opponent_model_metrics import build_strategy_intervention_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build strategy-intervention report.")
    parser.add_argument("--evaluation-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id")
    parser.add_argument(
        "--match-dir",
        action="append",
        dest="match_dirs",
        help="Explicit current-run match directory. Repeat to isolate a report run.",
    )
    args = parser.parse_args()
    summary = build_strategy_intervention_report(
        Path(args.evaluation_dir),
        Path(args.output_dir),
        run_id=args.run_id,
        match_dirs=args.match_dirs,
    )
    print(
        f"strategy-intervention report generated: {args.output_dir} "
        f"({summary['match_count']} matches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
