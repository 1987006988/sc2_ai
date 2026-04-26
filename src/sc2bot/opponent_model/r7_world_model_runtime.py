"""Pure-Python runtime for the exported R7 scratch-only world-model ensemble."""

from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path
from typing import Any

from sc2bot.domain.game_state import GameState
from sc2bot.domain.observations import ScoutingObservation

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


def _canonical_race_name(name: str) -> str:
    value = str(name or "unknown").strip().lower()
    mapping = {
        "protoss": "Protoss",
        "terran": "Terran",
        "zerg": "Zerg",
        "random": "Random",
    }
    return mapping.get(value, "Random")


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


def _live_own_frame(state: GameState, observation: ScoutingObservation) -> dict[str, Any]:
    return {
        "game_time": float(state.game_time),
        "expand_count": max(0, int(state.own_townhalls_count) - 1),
        "production_count": max(0, int(state.own_army_count) // 3),
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
    state: GameState,
    observation: ScoutingObservation,
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


class R7WorldModelRuntime:
    """Run the exported scratch-only ensemble without torch."""

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
            _linear(
                features,
                state_dict["encoder.0.weight"],
                state_dict["encoder.0.bias"],
            )
        )
        return _relu(
            _linear(
                hidden,
                state_dict["encoder.2.weight"],
                state_dict["encoder.2.bias"],
            )
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
        executable_actions: tuple[str, ...],
        opening_label: str,
        tech_label: str,
    ) -> tuple[str, dict[str, float], dict[str, Any]]:
        macro_mapping = label_encoders["macro_action_label"]
        future_winner_mapping = label_encoders["future_winner"]
        future_pressure_mapping = label_encoders["future_pressure_proxy"]
        future_length_mapping = label_encoders["future_game_length_bucket"]
        action_scores: dict[str, float] = {}
        action_payloads: dict[str, Any] = {}
        for action in executable_actions:
            action_index = int(macro_mapping[action])
            future_winner_probs = _softmax(
                self._future_logits(future_state, self.future_arm, action_index, "future_winner_head")
            )
            future_pressure_probs = _softmax(
                self._future_logits(future_state, self.future_arm, action_index, "future_pressure_head")
            )
            future_length_probs = _softmax(
                self._future_logits(
                    future_state,
                    self.future_arm,
                    action_index,
                    "future_game_length_head",
                )
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
        best_action = max(executable_actions, key=action_scores.__getitem__)
        return best_action, action_scores, action_payloads[best_action]

    def predict(
        self,
        state: GameState,
        observation: ScoutingObservation,
        *,
        executable_actions: tuple[str, ...],
    ) -> dict[str, Any]:
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

        opening_probs = _softmax(
            self._head_logits(hidden_state, self.hidden_macro_arm, "opening_head")
        )
        tech_probs = _softmax(self._head_logits(hidden_state, self.hidden_macro_arm, "tech_head"))
        macro_probs = _softmax(
            self._head_logits(hidden_state, self.hidden_macro_arm, "action_head")
        )
        tempo_probs = _softmax(
            self._head_logits(hidden_state, self.hidden_macro_arm, "tempo_head")
        )
        label_encoders = self.hidden_macro_arm["label_encoders"]
        opening_label = _decode(
            label_encoders["enemy_opening_class"], _argmax_index(opening_probs)
        )
        tech_label = _decode(label_encoders["enemy_tech_path"], _argmax_index(tech_probs))
        tempo_label = _decode(
            label_encoders["production_tempo_label"], _argmax_index(tempo_probs)
        )
        selected_action, action_scores, selected_future = self._candidate_scores(
            macro_probs,
            future_state,
            label_encoders,
            executable_actions,
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
            tech_risk = 0.65
        confidence = round(
            min(
                0.95,
                max(opening_probs) * 0.35 + max(tech_probs) * 0.35 + max(macro_probs) * 0.3,
            ),
            3,
        )
        return {
            "model_name": "r7_world_model_runtime_v0",
            "opening_type": opening_label,
            "tech_label": tech_label,
            "tempo_label": tempo_label,
            "recommended_macro_action": selected_action,
            "macro_action_scores": action_scores,
            "predicted_future_winner": selected_future["predicted_future_winner"],
            "predicted_future_pressure": selected_future["predicted_future_pressure"],
            "rush_risk": round(rush_risk, 3),
            "tech_risk": round(tech_risk, 3),
            "confidence": confidence,
            "signals": [
                "r7_world_model_runtime",
                f"opening:{opening_label}",
                f"tech:{tech_label}",
                f"tempo:{tempo_label}",
                f"macro_action:{selected_action}",
                f"future_pressure:{selected_future['predicted_future_pressure']}",
            ],
            "recommended_response_tags": (
                ("watch_for_rush",) if rush_risk >= 0.6 else ()
            ) + (("watch_for_tech",) if tech_risk >= 0.6 else ()),
        }
