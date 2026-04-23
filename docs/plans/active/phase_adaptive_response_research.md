
# Phase Adaptive Response Research

状态：active
更新日期：2026-04-23
进入条件：`checkpoint_E_level1_baseline_gate` 已通过
离开条件：`checkpoint_F_adaptive_research_gate` 已通过
直接依赖：

* `docs/foundation/04_research_direction/research_direction_decision.md`
* `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
* `docs/plans/active/research_master_task_queue.yaml`
* `docs/experiments/real_match_validation_protocol.md`
* `docs/experiments/checkpoint_acceptance_spec.md`

## 1. 本阶段只做一个研究问题

本阶段唯一允许的研究问题是：

在已接受的 `baseline_playable` 之上，是否可以构造一个 `scouting-conditioned belief state`，并让这个 belief state 只驱动少量、可解释、可归因的 `response gate`，从而在 matched paired evaluation 中产生真实行为差异，并在指定 slice 上带来方向一致的 outcome / robustness / failure-class 改善。

本阶段禁止把问题重新扩大成泛化的 “opponent modeling”。

本阶段不允许新增第二个研究特色。

## 2. 为什么只允许一个 research feature

只允许一个 research feature，原因不是保守，而是为了因果清晰：

1. 当前仓库刚从 playable baseline 阶段过渡过来，baseline 仍然宝贵且脆弱。
2. 当前最值得回答的问题不是“还能加多少花样”，而是“这一层 belief-driven response 到底有没有真实作用”。
3. 一旦同时引入 build order 重写、单位构成变化、micro 调整、LLM 决策或 learned model，就会失去可归因性。
4. 当前仓库已经有 `ScoutingObservation`、`OpponentPrediction`、`StrategyManager.select_response` 这些最小骨架；belief-driven response 是最贴近现有资产、最容易被证伪的方向。

## 3. 本阶段允许和禁止的内容

### 3.1 允许

1. 构造 typed belief state。
2. belief state 由 live scouting 和当前 game state 联合更新。
3. belief state 只影响少量 response gate。
4. paired control / treatment evaluation。
5. behavior delta 与 outcome delta 分开判定。

### 3.2 禁止

1. learned opponent model。
2. replay learning。
3. 全局 build order 重写。
4. 单位 composition policy 重写。
5. expansion 逻辑重写。
6. micro policy 重写。
7. broader-pool 展示驱动。
8. 用 telemetry 丰富度替代研究成功。

## 4. 文件边界和代码边界

### 4.1 belief state 的边界

首选新增文件：

* `src/sc2bot/domain/belief_state.py`

已有输入边界：

* `src/sc2bot/domain/observations.py`
* `src/sc2bot/domain/game_state.py`
* `src/sc2bot/opponent_model/interface.py`
* `src/sc2bot/opponent_model/null_model.py`
* `src/sc2bot/opponent_model/rule_based_model.py`

说明：

* belief state 必须是 typed object，不允许在 `strategy_manager.py` 里直接用 ad-hoc dict 作为长期主线结构。
* `ScoutingObservation` 继续负责 live scouting 事实。
* `OpponentPrediction` 继续负责模型输出。
* `BeliefState` 负责把“事实”和“推断”收束到一个可行动对象。

### 4.2 response layer 的边界

主要文件：

* `src/sc2bot/managers/strategy_manager.py`
* `src/sc2bot/managers/tactical_manager.py`
* `src/sc2bot/runtime/game_loop.py`
* `configs/bot/baseline_playable.yaml`
* `configs/bot/adaptive_research.yaml`

说明：

* `strategy_manager.py` 负责 belief -> gate 决策。
* `tactical_manager.py` 负责被允许的战术门控接入。
* `game_loop.py` 负责把 scouting gate 和 execution gate 接到真实行为。
* `adaptive_research.yaml` 是 treatment config；`baseline_playable.yaml` 是 control config。

### 4.3 evaluation 与 report 的边界

建议固定以下文件名：

* `configs/evaluation/r5_paired_control.yaml`
* `configs/evaluation/r5_paired_treatment.yaml`
* `artifacts/reports/r5_paired_adaptive_eval/report.md`
* `data/logs/evaluation/r5_paired_adaptive_eval/control/`
* `data/logs/evaluation/r5_paired_adaptive_eval/treatment/`

说明：

* 当前 runner 是单 bot_config 批运行；paired evaluation 应以两套 sibling config 组织，再在报告层面对齐。
* 不允许靠人工记忆去配对 control 和 treatment；必须在报告中显式写出 pair mapping。

## 5. belief state 的精确定义

## 5.1 belief state 的字段分类

### A. 来自 live scouting 的状态字段

这些字段直接来自 `ScoutingObservation`，属于事实状态，不属于推断：

1. `enemy_units_seen`
2. `enemy_structures_seen`
3. `enemy_expansions_seen`
4. `first_enemy_seen_time`
5. `last_enemy_seen_time`
6. `seen_enemy_structures`
7. `seen_enemy_combat_units`
8. `enemy_expansion_seen`
9. `possible_tech_signal`
10. `possible_rush_signal`
11. `observation_confidence`

这些字段的作用：

* 描述“看到了什么”和“多久没看到了”；
* 作为 belief update 的输入；
* 自身不能直接当 response gate 的唯一依据，必须与 game state 和 prediction 合并。

### B. 来自当前 game state 的状态字段

这些字段来自 `GameState`，属于当前局面状态，不是模型推断：

1. `game_time`
2. `known_enemy_start_location`
3. `visible_enemy_units_count`
4. `visible_enemy_structures_count`
5. `own_army_count`
6. `own_workers_count`
7. `minerals`
8. `vespene`
9. `supply_used`
10. `supply_cap`
11. `own_townhalls_count`

这些字段的作用：

* 描述 bot 当前能否安全继续 scout、是否适合 move-out、是否已经有军队基础；
* 为 response gate 提供安全边界；
* 不能被 treatment 任意重写。

### C. 来自 opponent model 的推断字段

这些字段来自 `OpponentPrediction`，属于推断，不属于事实状态：

1. `opening_type`
2. `rush_risk`
3. `tech_risk`
4. `enemy_army_estimate`
5. `confidence`
6. `signals`
7. `recommended_response_tags`

这些字段的作用：

* 提供“现在更像 rush、tech 还是信息不足”的推断；
* 允许进入 belief aggregation；
* 不允许直接绕过 gate 设计去重写全局策略。

### D. telemetry 辅助字段

这些字段允许存在，但不能单独构成研究 claim：

1. `model_name`
2. `prediction_mode`
3. `belief_version`
4. `decision_trace_id`
5. `gate_trace_id`
6. `debug_reason_chain`

这些字段的作用：

* 帮助排查和解释；
* 帮助 paired report 对齐；
* 不能作为“adaptive 成功”的主要证据。

## 5.2 建议的 BeliefState 字段集合

`BeliefState` 应至少包含以下字段，并显式标明哪类是状态、哪类是推断：

### 状态字段

1. `belief_time`
2. `scout_freshness_seconds`
3. `enemy_contact_known`
4. `enemy_expansion_seen`
5. `enemy_combat_seen`
6. `enemy_tech_signal_seen`
7. `known_enemy_start_location_available`
8. `own_army_ready`
9. `first_attack_currently_eligible`

### 推断字段

1. `rush_risk`
2. `tech_risk`
3. `information_confidence`
4. `information_gap_high`
5. `defensive_bias_active`
6. `scout_continuation_recommended`
7. `first_attack_timing_bias`

### telemetry 辅助字段

1. `model_name`
2. `prediction_mode`
3. `signal_summary`
4. `decision_trace_id`

## 5.3 belief 如何更新

每个 game loop 固定按以下顺序更新，不允许跨层乱改：

1. 构建 `GameState`。
2. 构建或刷新 `ScoutingObservation`。
3. 用当前 opponent model 得到 `OpponentPrediction`。
4. 将 `GameState`、`ScoutingObservation`、`OpponentPrediction` 合并成 `BeliefState`。
5. 用 `BeliefState` 决定 response gate。
6. 记录 `strategy_response` 与 `adaptive_gate_applied` telemetry。

禁止做法：

1. 直接让 `OpponentPrediction.recommended_response_tags` 控制行为；
2. 跳过 `BeliefState`，把 tag 直接塞进 `game_loop.py`；
3. 在 paired evaluation 中让 control 和 treatment 使用不同的 update 顺序。

## 6. response layer 的精确定义

## 6.1 response 最小集合

本阶段只允许以下三个 gate：

1. `continue_scouting_gate`
2. `defensive_posture_gate`
3. `first_attack_timing_gate`

除此之外，不允许新增第四个 gate。

## 6.2 每个 gate 的允许作用范围

### A. `continue_scouting_gate`

允许影响：

* `_safe_worker_scout` 是否在低信息状态下继续执行；
* 是否在信息过旧时补一次 scout；
* scout 是否在“可安全继续”的条件下延长最小持续时间。

不允许影响：

* scout 单位类型切换；
* 多 scout 并发；
* 自定义探路算法；
* 全图搜索策略。

### B. `defensive_posture_gate`

允许影响：

* 在高 rush risk 或高不确定性时，是否压制过早 move-out；
* army 是否优先保持 base-side posture；
* tactical planning 是否先走 defend-hold 分支。

不允许影响：

* build order 改写；
* 建筑位置重写；
* 单位 composition 重写；
* micro 行为重写。

### C. `first_attack_timing_gate`

允许影响：

* 首轮 attack order 的延后、保持或有限度提前；
* `attack_game_time_threshold` 或等价 attack eligibility 的运行时偏置；
* move-out 是否因 belief state 而推迟。

不允许影响：

* attack target selection 的整体逻辑；
* 多波次攻击策略；
* 全局战略切换；
* 在 `own_army_count=0` 时绕过 prerequisite 强行进攻。

## 6.3 response 不能过大

为了避免 response layer 变成“全局策略重写器”，本阶段禁止以下行为：

1. 通过 belief state 修改 worker economy。
2. 通过 belief state 修改 pylon / gateway / cyber build order。
3. 通过 belief state 改 zealot / stalker 生产优先级。
4. 通过 belief state 改扩张逻辑。
5. 通过 belief state 改 micro。
6. 通过 belief state 改地图特化脚本。

如果某项修改超出以上三个 gate，必须单独建新研究阶段，不得混入本阶段。

## 7. control / treatment 设计

## 7.1 control 是什么

control 固定为：

* `configs/bot/baseline_playable.yaml`

control 的要求：

1. 它必须是 `checkpoint_E` 接受过的 baseline control。
2. 它必须保持 build / production / tactical core 冻结。
3. 它可以继续记录 scouting、prediction、strategy telemetry，但 response gate 必须全部处于 neutral。
4. 不允许在 paired evaluation 期间继续修 baseline。

## 7.2 treatment 是什么

treatment 固定为：

* `configs/bot/adaptive_research.yaml`

treatment 的要求：

1. 它必须直接派生自 `baseline_playable.yaml`。
2. 除 adaptive gate 所需差异外，其余字段必须保持一致。
3. 允许变化的配置范围仅限：

   * `opponent_model.mode`
   * `opponent_model.intervention_mode`
   * 与 belief / gate 明确相关的新字段
4. 不允许借 treatment 顺便修 baseline core。

## 7.3 control 和 treatment 必须保持一致的部分

以下部分必须严格一致：

1. 代码版本
2. build chain
3. production chain
4. tactical core
5. map slice
6. opponent slice
7. evaluation contract
8. telemetry schema
9. artifact 目录结构
10. checkpoint 口径

若以上任一项不一致，paired evaluation 默认判为 `invalid_evidence`。

## 7.4 paired evaluation 该怎么组织

paired evaluation 按以下固定顺序执行：

1. 冻结 control baseline；
2. 创建 `r5_paired_control.yaml` 和 `r5_paired_treatment.yaml`；
3. 保证两者使用相同 maps / opponents / repeats / output schema；
4. 先跑 control，再跑 treatment，或反过来都可以，但 pair mapping 必须显式写入报告；
5. 报告中必须一一列出每个 pair：

   * map
   * opponent
   * control artifact path
   * treatment artifact path
   * behavior delta
   * outcome delta
   * failure-class delta
6. 先判断 behavior 是否真的改变，再判断 outcome 是否改善。

## 7.5 什么才算 “adaptive 改变了行为”

至少满足以下任一项，且有 paired 对照，才算 behavior change：

1. control 停止侦察，而 treatment 在低信息状态下继续侦察，并有真实 scout 行为差异；
2. treatment 在高 rush risk 下进入防守姿态，而 control 没有；
3. treatment 的首轮 `attack_order` 时间相对 control 发生可解释偏移；
4. paired report 中能明确指出 gate 触发 -> 行为变化 -> 对局差异的链条。

以下都不算 behavior change：

1. `strategy_response` tag 变了，但游戏内没有行为差异；
2. telemetry 更多了；
3. report 更丰富了；
4. 单次偶然 move-out timing 差异，且没有 gate trace 支撑。

## 8. claim 边界

## 8.1 可以说的 claim

1. “在指定 paired slice 上，adaptive gate 改变了继续侦察行为。”
2. “在指定 paired slice 上，adaptive gate 使首轮出击时机更晚 / 更早。”
3. “在指定 paired slice 上，adaptive gate 降低了某类 failure class。”
4. “在指定 paired slice 上，behavior delta 与 outcome 改善方向一致。”

## 8.2 不能说的 claim

1. “opponent modeling 已经成功。”
2. “telemetry richer，因此 adaptive 成功。”
3. “单次 anecdotal win 说明有研究贡献。”
4. “treatment 更强，所以 belief state 正确。”
5. “对更广泛对手池也有效。”（除非另有 extension batch）
6. “研究贡献已经成立。”（除非 `checkpoint_F` 通过）

## 8.3 behavior change 和 outcome improvement 必须分开判定

判定顺序固定如下：

1. 先判 paired evidence 是否有效；
2. 再判是否存在 behavior delta；
3. 最后才判是否有 outcome / robustness / failure-class improvement。

如果只有 outcome 差异、没有 behavior delta，不能接受研究 claim。
如果只有 behavior delta、没有 outcome 改善，可以接受“adaptive effect existed”，但不能接受“research contribution passed”。

## 9. 本阶段的执行顺序

## 9.1 work package A：冻结 control / treatment 合同

必须完成：

1. `baseline_playable.yaml` 冻结；
2. `adaptive_research.yaml` 创建；
3. paired control / treatment eval config 创建；
4. paired report 模板准备完毕。

本包未完成时，不允许写 adaptive code。

## 9.2 work package B：实现 belief state

必须完成：

1. `BeliefState` 类型定义；
2. `ScoutingObservation` + `GameState` + `OpponentPrediction` 的合并逻辑；
3. belief telemetry 输出；
4. state / inference / telemetry-only 字段分离清楚。

本包未完成时，不允许进入 response gate wiring。

## 9.3 work package C：接入 bounded response gate

必须完成：

1. `continue_scouting_gate` 接到真实 scout 行为；
2. `defensive_posture_gate` 接到真实 posture 行为；
3. `first_attack_timing_gate` 接到真实 move-out timing 行为；
4. control 与 treatment 的差异被限制在允许范围内。

本包未完成时，不允许进入 paired evaluation。

## 9.4 work package D：paired evaluation

必须完成：

1. control 和 treatment 的 paired artifacts 完整；
2. behavior delta 先被审核；
3. outcome / robustness / failure-class delta 再被审核；
4. `checkpoint_F_adaptive_research_gate` 决定通过或不通过。

## 10. minimum / target / stretch

## 10.1 minimum

minimum 定义：

1. adaptive layer 已不再是 telemetry-only；
2. 至少一个 gate 改变了真实行为；
3. baseline core 没被 treatment 破坏；
4. paired evidence 有效。

minimum 所需真实证据：

1. control / treatment 两侧完整 artifact；
2. 行为差异的时间线证据；
3. replay 或 telemetry 中的真实 scout / posture / attack timing 差异；
4. queue 中 `capability_validation_status` 不再是 `diagnostic_only`。

## 10.2 target

target 定义：

1. behavior delta 与 outcome / robustness / failure-class 改善方向一致；
2. paired report 能清楚归因到 adaptive gate；
3. `checkpoint_F` 正式接受研究结论。

target 所需真实证据：

1. matched pair 列表完整；
2. 每个 load-bearing pair 都可追溯；
3. 至少一个方向上的收益不是 anecdotal；
4. control / treatment 比较中没有 config drift 或 core drift。

## 10.3 stretch

stretch 定义：

1. 效果在多于一个 slice 上保持同方向，或
2. 三个允许 gate 中有两个以上能稳定工作，且仍然是同一个研究特色。

stretch 所需真实证据：

1. 第二个 slice 的 paired evidence；
2. 或第二个 gate 的稳定 paired behavior delta；
3. 不得引入新的 research feature。

## 11. 本阶段的失败入口

### adaptive 只改 telemetry，不改行为

返回：

* `task_016_integrate_single_adaptive_gating_layer`

### control 和 treatment 不可比

返回：

* paired eval config 冻结工作；
* 必要时 rerun `task_017_null_vs_adaptive_paired_evaluation`

### 有 behavior change，但没有 outcome benefit

先结论冻结为：

* `adaptive effect observed`
* `research contribution not accepted`

然后决定是否继续：

* 若 dominant 问题是 gate 过弱：返回 `task_016`
* 若 dominant 问题是 eval design：返回 `task_017` 重新组织 paired slice

### treatment 破坏 baseline core

立即回退到：

* `checkpoint_E` 接受过的 control 版本

不得带着漂移 baseline 继续做 paired evaluation。

## 12. 本阶段的完成定义

只有同时满足以下条件，本阶段才算完成：

1. `checkpoint_F_adaptive_research_gate` 通过；
2. paired evidence 明确显示 behavior delta；
3. paired evidence 明确显示方向一致的收益或鲁棒性改进；
4. 研究特色仍然只有一个；
5. 所有 claim 都保持在本文件允许的边界之内。

未满足以上条件时，项目最多只能说“已有 accepted playable baseline”，不能说“已有研究贡献”。
