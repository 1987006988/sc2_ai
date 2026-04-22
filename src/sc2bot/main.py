"""Command-line entrypoint for the SC2 bot skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path

from sc2bot.runtime.bot_app import BotApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the sc2-ai bot skeleton.")
    parser.add_argument(
        "--config",
        default="configs/bot/default.yaml",
        help="Path to bot config YAML.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Initialize dependencies without connecting to a StarCraft II runtime.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    app = BotApp.from_config(Path(args.config))
    if args.dry_run:
        app.initialize()
        return 0
    app.initialize()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
