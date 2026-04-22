"""Build the Phase A1 infrastructure-gate report from real probe/smoke outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_report(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Phase A1 Infrastructure Gate Report",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Evidence type: `{summary['evidence_type']}`",
        f"- Probe match count: `{summary['probe']['match_count']}`",
        f"- Smoke match count: `{summary['smoke']['total_matches']}`",
        f"- Smoke status counts: `{summary['smoke']['status_counts']}`",
        f"- Smoke crash rate: `{summary['smoke']['crash_rate']}`",
        f"- Smoke timeout rate: `{summary['smoke']['timeout_rate']}`",
        f"- Smoke artifact completeness rate: `{summary['smoke']['artifact_completeness_rate']}`",
        "",
        "## Evidence",
        "",
        f"- Probe manifest: `{summary['probe']['manifest_path']}`",
        f"- Smoke manifest: `{summary['smoke']['manifest_path']}`",
        f"- Failure accounting: `{summary['smoke']['failure_accounting_path']}`",
        "",
        "## Interpretation",
        "",
        "- The single probe validates the one-match real artifact chain.",
        "- The four-match smoke validates short multi-match orchestration and artifact persistence.",
        "- This is infrastructure evidence only.",
        "- One probe plus four smoke matches do not constitute a baseline dataset.",
        "- Phase A2 baseline dataset collection is still required before Phase A closeout.",
        "- This report does not prove bot strength, ladder competitiveness, or gameplay quality.",
        "",
        "## Real-Match-First Classification",
        "",
        "- Probe evidence: real match evidence.",
        "- Smoke evidence: real multi-match evidence.",
        "- Capability claim: infrastructure gate only.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_phase_a_a1_report(
    *,
    probe_dir: Path,
    smoke_dir: Path,
    output_dir: Path,
    run_id: str = "phase_a_a1_infrastructure_gate",
) -> dict[str, Any]:
    probe_manifest_path = probe_dir / "dataset_manifest.json"
    smoke_manifest_path = smoke_dir / "dataset_manifest.json"
    failure_accounting_path = smoke_dir / "failure_accounting_summary.json"
    probe_manifest = _read_json(probe_manifest_path)
    smoke_manifest = _read_json(smoke_manifest_path)
    failure_accounting = _read_json(failure_accounting_path)

    summary = {
        "run_id": run_id,
        "evidence_type": "real_infrastructure_gate",
        "probe": {
            "manifest_path": str(probe_manifest_path),
            "match_count": probe_manifest.get("match_count", 0),
            "status_counts": probe_manifest.get("status_counts", {}),
            "evidence_paths": probe_manifest.get("evidence_paths", []),
        },
        "smoke": {
            "manifest_path": str(smoke_manifest_path),
            "failure_accounting_path": str(failure_accounting_path),
            "total_matches": failure_accounting.get("total_matches", 0),
            "status_counts": failure_accounting.get("status_counts", {}),
            "crash_rate": failure_accounting.get("crash_rate"),
            "timeout_rate": failure_accounting.get("timeout_rate"),
            "artifact_completeness_rate": failure_accounting.get("artifact_completeness_rate"),
            "missing_replay_count": failure_accounting.get("missing_replay_count"),
            "missing_telemetry_count": failure_accounting.get("missing_telemetry_count"),
            "evidence_paths": failure_accounting.get("evidence_paths", []),
        },
        "limitations": [
            "infrastructure gate only",
            "one probe plus four smoke matches are not a baseline dataset",
            "does not prove bot strength",
            "does not prove ladder competitiveness",
            "does not prove gameplay quality",
            "Phase A2 baseline dataset is still required before Phase A closeout",
        ],
    }
    _write_json(output_dir / "summary.json", summary)
    _write_report(output_dir / "report.md", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Phase A1 infrastructure-gate report.")
    parser.add_argument("--probe-dir", required=True)
    parser.add_argument("--smoke-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="phase_a_a1_infrastructure_gate")
    args = parser.parse_args()
    summary = build_phase_a_a1_report(
        probe_dir=Path(args.probe_dir),
        smoke_dir=Path(args.smoke_dir),
        output_dir=Path(args.output_dir),
        run_id=args.run_id,
    )
    print(
        "phase-a-a1 report generated: "
        f"{args.output_dir} ({summary['smoke']['total_matches']} smoke matches)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
