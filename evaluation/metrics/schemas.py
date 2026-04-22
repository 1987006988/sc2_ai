"""Evaluation metric and result schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MatchMetrics:
    match_id: str
    result: str
    duration_seconds: float | None = None
    crashed: bool = False


@dataclass(frozen=True)
class MatchResult:
    match_id: str
    status: str
    result: str
    mode: str
    bot_name: str
    map_id: str
    opponent_id: str
    telemetry_path: str
    replay_metadata_path: str


@dataclass(frozen=True)
class MatchArtifactContract:
    """Canonical artifact contract for one evaluated match directory."""

    run_id: str
    match_id: str
    map_id: str
    opponent_id: str
    opponent_race: str | None
    opponent_difficulty: str | None
    bot_config_id: str
    start_time: str | None
    end_time: str | None
    status: str
    failure_reason: str | None
    replay_path: str | None
    telemetry_path: str | None
    match_result_path: str
    config_reference: str | None = None
    config_snapshot: dict[str, Any] | None = None
    sc2_version: str | None = None
    git_commit: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_match_result_payload(
        cls,
        payload: dict[str, Any],
        *,
        match_result_path: str,
        run_id: str | None = None,
    ) -> "MatchArtifactContract":
        """Build the contract from the current persisted match_result.json shape."""

        match_id = str(payload.get("match_id") or "")
        resolved_run_id = str(run_id or payload.get("run_id") or match_id)
        return cls(
            run_id=resolved_run_id,
            match_id=match_id,
            map_id=str(payload.get("map_id") or ""),
            opponent_id=str(payload.get("opponent_id") or ""),
            opponent_race=payload.get("opponent_race"),
            opponent_difficulty=payload.get("opponent_difficulty"),
            bot_config_id=str(payload.get("bot_config_id") or ""),
            start_time=payload.get("started_at") or payload.get("start_time"),
            end_time=payload.get("completed_at") or payload.get("end_time"),
            status=str(payload.get("status") or ""),
            failure_reason=payload.get("failure_reason"),
            replay_path=payload.get("replay_path"),
            telemetry_path=payload.get("telemetry_path"),
            match_result_path=match_result_path,
            config_reference=payload.get("config_reference") or payload.get("bot_config"),
            config_snapshot=payload.get("config_snapshot"),
            sc2_version=payload.get("sc2_version"),
            git_commit=payload.get("git_commit"),
            metadata={
                "mode": payload.get("mode"),
                "result": payload.get("result"),
                "opponent_model_mode": payload.get("opponent_model_mode"),
                "duration_seconds": payload.get("duration_seconds"),
            },
        )

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        required_values = {
            "run_id": self.run_id,
            "match_id": self.match_id,
            "map_id": self.map_id,
            "opponent_id": self.opponent_id,
            "bot_config_id": self.bot_config_id,
            "status": self.status,
            "match_result_path": self.match_result_path,
        }
        for field_name, value in required_values.items():
            if not value:
                errors.append(f"missing required field: {field_name}")
        if not (self.config_reference or self.config_snapshot):
            errors.append("missing config_reference or config_snapshot")
        return errors


@dataclass(frozen=True)
class ArtifactCompleteness:
    match_result_count: int = 0
    replay_count: int = 0
    telemetry_count: int = 0
    missing_match_result_count: int = 0
    missing_replay_count: int = 0
    missing_telemetry_count: int = 0


@dataclass(frozen=True)
class DatasetManifest:
    """Versioned manifest schema for a scoped real-match dataset run."""

    run_id: str
    created_at: str
    purpose: str
    included_match_dirs: tuple[str, ...]
    excluded_historical_dirs: tuple[str, ...]
    map_pool: tuple[str, ...]
    opponent_pool: tuple[str, ...]
    bot_configs: tuple[str, ...]
    config_snapshot: dict[str, Any]
    match_count: int
    status_counts: dict[str, int]
    artifact_completeness: ArtifactCompleteness
    evidence_paths: tuple[str, ...]
    chunk_run_ids: tuple[str, ...] = ()
    source_manifests: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        required_values = {
            "run_id": self.run_id,
            "created_at": self.created_at,
            "purpose": self.purpose,
        }
        for field_name, value in required_values.items():
            if not value:
                errors.append(f"missing required field: {field_name}")
        if self.match_count != len(self.included_match_dirs):
            errors.append(
                "match_count must equal the number of included_match_dirs"
            )
        if sum(self.status_counts.values()) != self.match_count:
            errors.append("status_counts must sum to match_count")
        if not self.evidence_paths:
            errors.append("missing evidence_paths")
        return errors
