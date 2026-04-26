"""Self-contained R7 macro advisor for sludge-revived runtime."""

from __future__ import annotations

import json
import math
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bot.model.scouting_information import ScoutingInformation

_RACES = ("Protoss", "Terran", "Zerg", "Random")
_TASK_NAMES = (
    "enemy_opening_class",
    "enemy_tech_path",
    "macro_action_label",
    "production_tempo_label",
    "future_winner",
    "future_game_length_bucket",
    "future_pressure_proxy",
)
_EXECUTABLE_ACTIONS = (
    "add_production",
    "add_tech",
    "increase_production_tempo",
    "defensive_hold",
    "move_out_window_open",
    "delay_move_out",
)


@dataclass(frozen=True)
class AdvisorState:
    game_time: float
    own_race: str
    enemy_race: str
    visible_enemy_units_count: int = 0
    visible_enemy_structures_count: int = 0
    visible_enemy_units: tuple[str, ...] = field(default_factory=tuple)
    visible_enemy_structures: tuple[str, ...] = field(default_factory=tuple)
    visible_enemy_townhalls_count: int = 0
    own_workers_count: int = 0
    own_army_count: int = 0
    own_townhalls_count: int = 0
    own_army_value: float = 0.0
    enemy_army_value: float = 0.0
    minerals: int = 0
    vespene: int = 0
    supply_used: int = 0
    supply_cap: int = 0


@dataclass(frozen=True)
class AdvisorObservation:
    current_enemy_units: tuple[str, ...] = field(default_factory=tuple)
    current_enemy_structures: tuple[str, ...] = field(default_factory=tuple)
    current_enemy_combat_units: tuple[str, ...] = field(default_factory=tuple)
    enemy_units_seen: tuple[str, ...] = field(default_factory=tuple)
    enemy_structures_seen: tuple[str, ...] = field(default_factory=tuple)
    enemy_expansions_seen: int = 0
    possible_tech_signal: bool = False
    possible_rush_signal: bool = False
    observation_confidence: float = 0.0


@dataclass(frozen=True)
class AdvisorPrediction:
    model_name: str
    recommended_macro_action: str
    macro_action_scores: dict[str, float]
    confidence: float
    rush_risk: float
    tech_risk: float
    opening_type: str = "unknown"
    predicted_future_winner: str = "unknown"
    predicted_future_pressure: str = "unknown"
    prediction_mode: str = "none"
    signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdvisorResponse:
    selected_macro_action: str
    continue_scouting: bool
    defensive_posture: bool
    force_attack_mode: bool
    production_tempo_delta: int
    force_add_tech: bool
    proxy_scout_target_count: int
    confidence: float
    rush_risk: float
    tech_risk: float
    prediction_mode: str
    signals: tuple[str, ...]
    macro_action_scores: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "selected_macro_action": self.selected_macro_action,
            "continue_scouting": self.continue_scouting,
            "defensive_posture": self.defensive_posture,
            "force_attack_mode": self.force_attack_mode,
            "production_tempo_delta": self.production_tempo_delta,
            "force_add_tech": self.force_add_tech,
            "proxy_scout_target_count": self.proxy_scout_target_count,
            "confidence": self.confidence,
            "rush_risk": self.rush_risk,
            "tech_risk": self.tech_risk,
            "prediction_mode": self.prediction_mode,
            "signals": list(self.signals),
            "macro_action_scores": self.macro_action_scores,
        }


def _canonical_race_name(name: str) -> str:
    value = str(name or "unknown").strip().lower()
    mapping = {
        "protoss": "Protoss",
        "terran": "Terran",
        "zerg": "Zerg",
        "random": "Random",
    }
    return mapping.get(value, "Random")


def build_state_snapshot(state_service) -> tuple[AdvisorState, AdvisorObservation]:
    bot = state_service._bot
    enemy_units = tuple(sorted({u.type_id.name for u in state_service.enemy_units}))
    enemy_structures = tuple(sorted({u.type_id.name for u in state_service.enemy_structures}))
    enemy_combat_units = tuple(sorted({u.type_id.name for u in state_service.enemy_army_units}))
    possible_rush_signal = (
        ScoutingInformation.ENEMY_ONE_BASE in state_service.scouting_information
        or ScoutingInformation.THREAT_LEVEL_1 in state_service.scouting_information
        or ScoutingInformation.ENEMY_MOVED_OUT in state_service.scouting_information
    )
    possible_tech_signal = bool(state_service.enemy_tech) or any(
        marker in state_service.scouting_information
        for marker in (
            ScoutingInformation.THREAT_CLOAK,
            ScoutingInformation.STARGATE,
            ScoutingInformation.STARPORT_TECHLAB,
        )
    )
    confidence = 0.2
    if enemy_units or enemy_structures:
        confidence = 0.65
    elif possible_tech_signal or possible_rush_signal:
        confidence = 0.45
    state = AdvisorState(
        game_time=state_service.getTimeInSeconds(),
        own_race=_canonical_race_name(bot.race.name),
        enemy_race=_canonical_race_name(bot.enemy_race.name),
        visible_enemy_units_count=state_service.enemy_units.amount,
        visible_enemy_structures_count=state_service.enemy_structures.amount,
        visible_enemy_units=enemy_units,
        visible_enemy_structures=enemy_structures,
        visible_enemy_townhalls_count=state_service.enemy_townhalls.amount,
        own_workers_count=state_service.drone_count,
        own_army_count=state_service.own_army_units.amount,
        own_townhalls_count=state_service.own_townhalls.amount,
        own_army_value=float(state_service.own_army_value),
        enemy_army_value=float(state_service.enemy_army_value),
        minerals=int(state_service.resources.minerals),
        vespene=int(state_service.resources.vespene),
        supply_used=int(state_service.resources.supply.used),
        supply_cap=int(state_service.resources.supply.cap),
    )
    observation = AdvisorObservation(
        current_enemy_units=enemy_units,
        current_enemy_structures=enemy_structures,
        current_enemy_combat_units=enemy_combat_units,
        enemy_units_seen=enemy_units,
        enemy_structures_seen=enemy_structures,
        enemy_expansions_seen=max(0, state_service.enemy_townhalls.amount - 1),
        possible_tech_signal=possible_tech_signal,
        possible_rush_signal=possible_rush_signal,
        observation_confidence=confidence,
    )
    return state, observation


class RuleMacroAdvisor:
    model_name = "r7_rule_macro_advisor"

    def predict(self, state: AdvisorState, observation: AdvisorObservation) -> AdvisorPrediction:
        if observation.possible_rush_signal or state.visible_enemy_units_count > 0:
            action = "defensive_hold"
            rush_risk = 0.7
            tech_risk = 0.2
        elif observation.possible_tech_signal:
            action = "add_tech"
            rush_risk = 0.25
            tech_risk = 0.65
        elif state.own_army_count < 8:
            action = "add_production"
            rush_risk = 0.25
            tech_risk = 0.2
        elif state.game_time >= 320.0 and state.own_army_count >= 12:
            action = "move_out_window_open"
            rush_risk = 0.15
            tech_risk = 0.2
        else:
            action = "delay_move_out"
            rush_risk = 0.2
            tech_risk = 0.2
        scores = {name: 0.2 for name in _EXECUTABLE_ACTIONS}
        scores[action] = 0.8
        return AdvisorPrediction(
            model_name=self.model_name,
            recommended_macro_action=action,
            macro_action_scores=scores,
            confidence=0.55,
            rush_risk=rush_risk,
            tech_risk=tech_risk,
            opening_type="rule_based_macro",
            predicted_future_winner="unknown",
            predicted_future_pressure="high_pressure" if action == "defensive_hold" else "low_pressure",
            prediction_mode="rule_macro_advisor",
            signals=(f"macro_action:{action}",),
        )


def _one_hot(value: str, vocab: tuple[str, ...]) -> list[float]:
    return [1.0 if value == candidate else 0.0 for candidate in vocab]


def _linear(vector: list[float], weight: list[list[float]], bias: list[float]) -> list[float]:
    return [
        sum(component * coeff for component, coeff in zip(vector, row)) + bias[idx]
        for idx, row in enumerate(weight)
    ]


def _relu(vector: list[float]) -> list[float]:
    return [max(0.0, value) for value in vector]


def _softmax(logits: list[float]) -> list[float]:
    max_logit = max(logits)
    numerators = [math.exp(value - max_logit) for value in logits]
    denom = sum(numerators) or 1.0
    return [value / denom for value in numerators]


def _argmax_index(values: list[float]) -> int:
    return max(range(len(values)), key=values.__getitem__)


def _decode(mapping: dict[str, int], index: int) -> str:
    reverse = {int(idx): label for label, idx in mapping.items()}
    return reverse[index]


def _live_own_frame(state: AdvisorState, observation: AdvisorObservation) -> dict[str, Any]:
    return {
        "game_time": float(state.game_time),
        "expand_count": max(0, int(state.own_townhalls_count) - 1),
        "production_count": max(0, int(state.own_army_count) // 6),
        "tech_count": 1 if int(state.vespene) > 0 else 0,
        "upgrade_count": 0,
        "defense_count": 1 if int(state.visible_enemy_units_count) > 0 else 0,
        "combat_unit_count": int(state.own_army_count),
        "worker_econ_count": int(state.own_workers_count),
        "attack_count": (
            1
            if int(state.own_army_count) > 0 and int(state.visible_enemy_units_count) > 0
            else 0
        ),
    }


def _build_runtime_sample(
    state: AdvisorState,
    observation: AdvisorObservation,
    frames: list[dict[str, Any]],
    *,
    global_priors: dict[str, Any],
    rule_tables: dict[str, dict[str, Any]],
    label_encoders: dict[str, dict[str, int]],
) -> dict[str, Any]:
    own_frame = _live_own_frame(state, observation)
    sample = {
        "game_time": float(state.game_time),
        "own_visible_state": {
            "own_race": _canonical_race_name(state.own_race),
            "expand_count": own_frame["expand_count"],
            "production_count": own_frame["production_count"],
            "tech_count": own_frame["tech_count"],
            "upgrade_count": own_frame["upgrade_count"],
            "defense_count": own_frame["defense_count"],
            "combat_unit_count": own_frame["combat_unit_count"],
            "worker_econ_count": own_frame["worker_econ_count"],
            "attack_count": own_frame["attack_count"],
        },
        "observed_enemy_state": {
            "enemy_race": _canonical_race_name(state.enemy_race),
        },
        "frames": frames,
    }
    key = (
        f"{sample['own_visible_state']['own_race']}|"
        f"{sample['observed_enemy_state']['enemy_race']}"
    )
    priors = dict(rule_tables.get(key, global_priors))
    prior_features: list[float] = []
    for task in _TASK_NAMES:
        mapping = label_encoders[task]
        predicted = str(priors[task])
        index = int(mapping[predicted])
        prior_features.extend(1.0 if idx == index else 0.0 for idx in range(len(mapping)))
    sample["_rule_prior_features"] = prior_features
    return sample


def _feature_vector(sample: dict[str, Any]) -> list[float]:
    own = sample["own_visible_state"]
    observed_enemy = sample["observed_enemy_state"]
    vector = [
        float(own["expand_count"]),
        float(own["production_count"]),
        float(own["tech_count"]),
        float(own["upgrade_count"]),
        float(own["defense_count"]),
        float(own["combat_unit_count"]),
        float(own["worker_econ_count"]),
        float(own["attack_count"]),
    ]
    for frame in sample["frames"]:
        vector.extend(
            [
                float(frame["expand_count"]),
                float(frame["production_count"]),
                float(frame["tech_count"]),
                float(frame["upgrade_count"]),
                float(frame["defense_count"]),
                float(frame["combat_unit_count"]),
                float(frame["worker_econ_count"]),
                float(frame["attack_count"]),
            ]
        )
    vector.extend(_one_hot(own["own_race"], _RACES))
    vector.extend(_one_hot(observed_enemy["enemy_race"], _RACES))
    vector.append(float(sample["game_time"]))
    vector.extend(float(value) for value in sample.get("_rule_prior_features", ()))
    return vector


class WorldModelRuntime:
    def __init__(self, runtime_path: str | Path, *, history_window: int = 3) -> None:
        self.runtime_path = Path(runtime_path)
        self.payload = json.loads(self.runtime_path.read_text(encoding="utf-8"))
        self.history_window = max(1, int(history_window))
        self._frames: deque[dict[str, Any]] = deque(maxlen=self.history_window)
        self.hidden_macro_arm = self.payload["components"]["hidden_macro_arm"]
        self.future_arm = self.payload["components"]["future_arm"]

    def _encode_arm(self, component: dict[str, Any], features: list[float]) -> list[float]:
        state_dict = component["state_dict"]
        hidden = _relu(
            _linear(features, state_dict["encoder.0.weight"], state_dict["encoder.0.bias"])
        )
        return _relu(
            _linear(hidden, state_dict["encoder.2.weight"], state_dict["encoder.2.bias"])
        )

    def _head_logits(self, state: list[float], component: dict[str, Any], prefix: str) -> list[float]:
        state_dict = component["state_dict"]
        return _linear(state, state_dict[f"{prefix}.weight"], state_dict[f"{prefix}.bias"])

    def _future_logits(
        self,
        state: list[float],
        component: dict[str, Any],
        action_index: int,
        prefix: str,
    ) -> list[float]:
        state_dict = component["state_dict"]
        model_cfg = component["model_config"]
        if model_cfg.get("use_action_conditioning", True):
            action_embedding = state_dict["action_embedding.weight"][action_index]
            future_input = list(state) + list(action_embedding)
        else:
            future_input = list(state)
        return _linear(future_input, state_dict[f"{prefix}.weight"], state_dict[f"{prefix}.bias"])

    def _candidate_scores(
        self,
        macro_probs: list[float],
        future_state: list[float],
        label_encoders: dict[str, dict[str, int]],
        opening_label: str,
        tech_label: str,
    ) -> tuple[str, dict[str, float], dict[str, Any]]:
        macro_mapping = label_encoders["macro_action_label"]
        future_winner_mapping = label_encoders["future_winner"]
        future_pressure_mapping = label_encoders["future_pressure_proxy"]
        future_length_mapping = label_encoders["future_game_length_bucket"]
        action_scores: dict[str, float] = {}
        action_payloads: dict[str, Any] = {}
        for action in _EXECUTABLE_ACTIONS:
            action_index = int(macro_mapping[action])
            future_winner_probs = _softmax(
                self._future_logits(future_state, self.future_arm, action_index, "future_winner_head")
            )
            future_pressure_probs = _softmax(
                self._future_logits(future_state, self.future_arm, action_index, "future_pressure_head")
            )
            future_length_probs = _softmax(
                self._future_logits(future_state, self.future_arm, action_index, "future_game_length_head")
            )
            win_p = future_winner_probs[future_winner_mapping["win"]]
            low_pressure_p = future_pressure_probs[future_pressure_mapping["low_pressure"]]
            long_game_p = future_length_probs[future_length_mapping["long"]]
            score = 0.45 * macro_probs[action_index] + 0.35 * win_p + 0.2 * low_pressure_p
            if action == "defensive_hold" and opening_label == "pressure_open":
                score += 0.12
            if action == "add_tech" and tech_label in {"tech_path_present", "upgrade_path"}:
                score += 0.08
            if action == "move_out_window_open" and opening_label == "pressure_open":
                score -= 0.18
            if action == "delay_move_out":
                score += 0.05 * long_game_p
            action_scores[action] = round(score, 6)
            action_payloads[action] = {
                "predicted_future_winner": _decode(
                    future_winner_mapping, _argmax_index(future_winner_probs)
                ),
                "predicted_future_pressure": _decode(
                    future_pressure_mapping, _argmax_index(future_pressure_probs)
                ),
            }
        best_action = max(_EXECUTABLE_ACTIONS, key=action_scores.__getitem__)
        return best_action, action_scores, action_payloads[best_action]

    def predict(self, state: AdvisorState, observation: AdvisorObservation) -> AdvisorPrediction:
        self._frames.append(_live_own_frame(state, observation))
        frames = list(self._frames)
        while len(frames) < self.history_window:
            frames.insert(0, dict(frames[0] if frames else _live_own_frame(state, observation)))
        sample = _build_runtime_sample(
            state,
            observation,
            frames,
            global_priors=self.payload["global_priors"],
            rule_tables=self.payload["rule_tables"],
            label_encoders=self.hidden_macro_arm["label_encoders"],
        )
        features = _feature_vector(sample)
        hidden_state = self._encode_arm(self.hidden_macro_arm, features)
        future_state = self._encode_arm(self.future_arm, features)
        opening_probs = _softmax(self._head_logits(hidden_state, self.hidden_macro_arm, "opening_head"))
        tech_probs = _softmax(self._head_logits(hidden_state, self.hidden_macro_arm, "tech_head"))
        macro_probs = _softmax(self._head_logits(hidden_state, self.hidden_macro_arm, "action_head"))
        tempo_probs = _softmax(self._head_logits(hidden_state, self.hidden_macro_arm, "tempo_head"))
        label_encoders = self.hidden_macro_arm["label_encoders"]
        opening_label = _decode(label_encoders["enemy_opening_class"], _argmax_index(opening_probs))
        tech_label = _decode(label_encoders["enemy_tech_path"], _argmax_index(tech_probs))
        tempo_label = _decode(label_encoders["production_tempo_label"], _argmax_index(tempo_probs))
        selected_action, action_scores, selected_future = self._candidate_scores(
            macro_probs,
            future_state,
            label_encoders,
            opening_label,
            tech_label,
        )
        pressure_high = selected_future["predicted_future_pressure"] == "high_pressure"
        rush_risk = 0.2
        if opening_label == "pressure_open":
            rush_risk = 0.68
        elif pressure_high:
            rush_risk = 0.55
        tech_risk = 0.2
        if tech_label in {"tech_path_present", "upgrade_path"}:
            tech_risk = 0.64
        elif tempo_label == "high_tempo":
            tech_risk = 0.45
        confidence = round(max(action_scores.values()), 6)
        return AdvisorPrediction(
            model_name="r7_world_model_runtime_v0",
            recommended_macro_action=selected_action,
            macro_action_scores=action_scores,
            confidence=confidence,
            rush_risk=rush_risk,
            tech_risk=tech_risk,
            opening_type=opening_label,
            predicted_future_winner=selected_future["predicted_future_winner"],
            predicted_future_pressure=selected_future["predicted_future_pressure"],
            prediction_mode="learned_world_model_advisor",
            signals=(
                f"opening:{opening_label}",
                f"tech:{tech_label}",
                f"tempo:{tempo_label}",
                f"selected_action:{selected_action}",
            ),
        )


def response_from_prediction(state: AdvisorState, observation: AdvisorObservation, prediction: AdvisorPrediction) -> AdvisorResponse:
    action = prediction.recommended_macro_action
    continue_scouting = (
        prediction.confidence <= 0.35
        or observation.observation_confidence <= 0.35
        or not observation.enemy_units_seen
    )
    defensive_posture = action in {"defensive_hold", "delay_move_out"}
    force_attack_mode = (
        action == "move_out_window_open"
        and state.own_army_count >= 10
        and state.own_army_value >= max(150.0, 0.8 * state.enemy_army_value)
    )
    production_tempo_delta = 0
    if action == "add_production":
        production_tempo_delta = 1
    elif action == "increase_production_tempo":
        production_tempo_delta = 2
    force_add_tech = action == "add_tech"
    proxy_scout_target_count = 6 if continue_scouting else 4
    return AdvisorResponse(
        selected_macro_action=action,
        continue_scouting=continue_scouting,
        defensive_posture=defensive_posture,
        force_attack_mode=force_attack_mode,
        production_tempo_delta=production_tempo_delta,
        force_add_tech=force_add_tech,
        proxy_scout_target_count=proxy_scout_target_count,
        confidence=prediction.confidence,
        rush_risk=prediction.rush_risk,
        tech_risk=prediction.tech_risk,
        prediction_mode=prediction.prediction_mode,
        signals=prediction.signals,
        macro_action_scores=prediction.macro_action_scores,
    )
