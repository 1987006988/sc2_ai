# Failed Attempts

## 2026-04-17: Package-first framework validation is blocked by environment availability

### Context

Tried to validate both Ares-sc2 and bare python-sc2 through local imports and package resolution.

### Observation

Neither `ares` nor `sc2` is currently installed, and the current environment does not resolve `sc2` or `ares-sc2` through pip dry-run checks.

### Conclusion

Do not block phase-1 startup on Ares-sc2 availability. Prefer the thinner python-sc2 target and continue with project-local runtime and evaluation work.

### Action Rule

Treat framework availability as an environment integration task, not as a reason to stall the rest of phase-1 scaffolding.

## 2026-04-17: Real launch validation still stops above the bot package layer

### Context

Added SC2PATH-based preflight and a real-launch branch in evaluation.

### Observation

The local SC2 installation root is known and preflightable, and the project can launch `StarCraft II.exe` for process validation. However, the repository still does not have a verified python-sc2-backed runtime launch path.

### Conclusion

The current bottleneck is no longer SC2 root discovery or raw process launch. It is the missing verified bot package/runtime integration layer for real match orchestration.

### Action Rule

Focus next on the real runtime adapter rather than expanding evaluation features.

## 2026-04-17: Direct pip install from pypi.org failed during runtime enablement

### Context

Tried to install the phase-1 bare python-sc2 base directly from the default PyPI endpoint.

### Observation

The environment hit SSL failures against `pypi.org`, so the direct install path did not work reliably.

### Conclusion

When dependency installation is part of runtime enablement on this machine, prefer the configured Tsinghua mirror instead of assuming direct PyPI access.

### Action Rule

If `python -m pip install ...` fails with SSL or index resolution issues, retry with the documented mirror before treating the package as unavailable.
