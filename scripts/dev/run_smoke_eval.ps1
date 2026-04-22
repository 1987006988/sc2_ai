$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src;."
python evaluation/runner/run_batch.py --config configs/evaluation/smoke.yaml
