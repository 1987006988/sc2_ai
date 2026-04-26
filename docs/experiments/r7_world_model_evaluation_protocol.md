# R7 World Model Evaluation Protocol

Status: active
Updated: 2026-04-26
Role: defines offline, online, and external evaluation rules for the R7
counterfactual macro world model.

## Evidence Layers

R7 requires all three:

1. teacher-data offline benchmark
2. strong-substrate online intervention
3. external bot ecosystem validation

No single layer substitutes for the others.

## Offline Task Groups

The offline benchmark must cover:

1. hidden-state tasks
2. macro-action tasks
3. future or counterfactual-proxy tasks

## Required Offline Comparators

At minimum compare:

1. static prior
2. rule-based baseline
3. shallow temporal baseline
4. scratch learned world model
5. optional warm-start or external baseline

## Online Arms

Online evaluation must use:

1. Arm A: original strong substrate
2. Arm B: strong substrate plus rule-based macro advisor
3. Arm C: strong substrate plus learned world-model macro advisor

## Online Behavior Delta

Valid behavior deltas include changes in:

1. expansion timing
2. tech timing
3. production scaling
4. detection timing
5. composition bias
6. defensive hold or move-out timing
7. scout or rescout behavior

## Online Target Standard

Online target requires:

1. repeated behavior difference for Arm C;
2. preserved strong-bot core;
3. outcome or robustness improvement relative to Arm A or Arm B;
4. a causal link between model-driven macro actions and the observed result.

## External Minimum

External validation requires:

1. at least one valid external slice;
2. complete replay, result, and log artifacts;
3. at least Arm A/C or full A/B/C comparability.

## Invalid Evidence

Evidence is invalid if:

1. strong-bot version drift exists;
2. A/B/C are not comparable;
3. strong-bot core was modified without disclosure;
4. replay or results are missing;
5. data leakage exists;
6. invalid runs are mixed into accepted tables.
