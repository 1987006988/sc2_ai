from pathlib import Path

from sc2bot.runtime.bot_app import BotApp


def test_bot_app_dry_initializes(tmp_path, monkeypatch):
    monkeypatch.chdir(Path.cwd())
    app = BotApp.from_config(Path("configs/bot/debug.yaml"))
    app.config.telemetry.output_dir
    app.initialize()

    assert app.config.bot.name == "sc2-ai-debug"
