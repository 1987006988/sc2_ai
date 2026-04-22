$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src;."
python -m ruff check src evaluation tests
