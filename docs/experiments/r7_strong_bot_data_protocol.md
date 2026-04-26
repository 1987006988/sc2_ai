# R7 Strong Bot Data Protocol

Status: active
Updated: 2026-04-26
Role: governs strong bot acquisition, strong replay data usage, and teacher
dataset materialization.

## Purpose

R7 allows use of strong third-party bots and strong replay data, but prevents:

1. credit leakage from downloaded bot strength into our claim;
2. license misuse;
3. replay or comparator leakage into training or holdout evidence.

## Candidate Roles

Each strong candidate must be classified as one or more of:

1. `substrate`
2. `teacher`
3. `comparator`

## Required Audit Fields

Every candidate must record:

1. candidate id
2. source name
3. source type
4. source reference
5. license
6. license status
7. intended role
8. game version
9. race
10. framework
11. local run status
12. replay availability
13. logs availability
14. action trace availability
15. intervention feasibility
16. strength evidence
17. data volume estimate
18. risks
19. decision

## License Rules

Before license audit completes:

1. do not vendor code;
2. do not modify the candidate as mainline work;
3. do not use its data for training;
4. do not promote it from candidate to accepted substrate.

## Split Rules

1. the same replay cannot appear in train and test;
2. same-series or same-time-window replay leakage is forbidden;
3. external evaluation opponents cannot enter training;
4. accepted R4 and R5 repository artifacts remain domain anchors only, not main
   R7 holdout evidence.

## Required Teacher Sample Fields

Each materialized sample must contain at least:

1. `sample_id`
2. `source_id`
3. `replay_id`
4. `game_time`
5. `map`
6. `matchup`
7. `own_visible_state`
8. `observed_enemy_state`
9. `hidden_enemy_label`
10. `macro_action_label`
11. `candidate_action_slate`
12. `future_outcome_label`
13. `winner`
14. `split`
15. `provenance`

## Minimum Passing Standard

1. at least one strong source provides valid replay or log data;
2. source provenance is complete;
3. split policy is explicit;
4. hidden-state and macro-action labels are at least partially extractable.
