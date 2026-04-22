# Interview Positioning

This file defines how to present the project in interviews. It is a presentation-layer document, not an engineering rule file.

## One-line Introduction

A full-game StarCraft II AI that models hidden opponent intent under fog of war, adapts strategy online, and explains its decisions after the match.

## Why This Project Stands Out

### Compared with a scripted bot

- It does not only execute fixed build orders.
- It makes explicit opponent-state estimates under fog of war.
- It can adapt strategy based on inferred risk and intent.
- It has a clearer explanation chain from scouting to strategy choice.

### Compared with a pure SMAC / benchmark project

- It is a full-game system rather than only a micro-control experiment.
- It demonstrates agent architecture, runtime design, telemetry, evaluation, and adaptation together.
- It is easier to explain as a complete AI system rather than a single benchmark result.

### Compared with a pure LLM project

- The core gameplay logic remains measurable and evaluable.
- The main research question is grounded in SC2 itself: partial observability and hidden intent.
- LLM usage stays in the replay-analysis or coach layer, where it is more credible and more stable.

## Why It Is Interesting

- It targets a real SC2 problem instead of a generic AI demo.
- It can produce both technical evidence and compelling demonstrations.
- It combines bot engineering, partial-observability reasoning, evaluation design, and explainability.

## Important Boundary

This positioning must not be used to justify:

- moving LLMs into real-time control;
- moving SMAC code into `src/sc2bot/`;
- expanding phase 1 into end-to-end RL or full world-model work.
