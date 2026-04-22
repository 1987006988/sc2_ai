$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"
python -m sc2bot.main --config configs/bot/debug.yaml --dry-run
