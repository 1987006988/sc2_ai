$ErrorActionPreference = "Stop"
Write-Host "Python:"
python --version
Write-Host "Pip:"
python -m pip --version
$env:PYTHONPATH = "src;."
Write-Host "SC2PATH: $env:SC2PATH"
@'
from sc2bot.runtime.sc2_installation import run_sc2_preflight
result = run_sc2_preflight()
print(result.to_dict())
'@ | python -
Write-Host "Repository and SC2 preflight check complete."
