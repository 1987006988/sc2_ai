
# Phase Playable Core Rebuild

状态：active
更新日期：2026-04-23
进入条件：`checkpoint_A_start_gate` 已通过
离开条件：`checkpoint_E_level1_baseline_gate` 已通过
直接依赖：

* `docs/foundation/04_research_direction/research_direction_decision.md`
* `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
* `docs/plans/active/research_master_task_queue.yaml`
* `docs/experiments/real_match_validation_protocol.md`
* `docs/experiments/checkpoint_acceptance_spec.md`

## 1. 阶段目标

本阶段的唯一目标，是把项目从“能够跑真实 SC2、有 telemetry、有长窗口”推进到“真正可玩的 non-adaptive baseline”。

本阶段结束时，必须至少具备以下真实能力：

1. opening build chain 成立。
2. Gateway ready 成立。
3. combat-unit production 成立。
4. `own_army_count > 0` 成立。
5. rally / defend / attack 至少部分成立，而且不建立在假 army 上。
6. `friendly combat` 有真实验证机会，并且不再只剩 enemy-visible signal。
7. easy slice 上的 small eval 不再只是 diagnostic-only，而是能支撑 Level 1 baseline 决策。

本阶段只处理两类内容：

1. infrastructure -> gameplay capability 的转化；
2. gameplay capability 的真实验收。

本阶段不处理：

1. adaptive research claim；
2. learned opponent model；
3. broader pool 展示；
4. ladder 竞争力叙述；
5. README 包装。

## 2. 当前执行前提

本文件默认以下前提已经成立：

1. 真实本地对局可启动。
2. replay / result / telemetry 可落盘。
3. 长窗口运行前提已经被重新验证过一次。
4. 旧 Phase B 的命令级信号不能再当作能力通过。
5. 当前 gameplay 主线仍以 `src/sc2bot/runtime/game_loop.py` 为中心，尚未形成成熟的 manager 分层。

如果以上任一项不成立，本阶段不得开始，必须先回到 `phase_r0_execution_freeze` 相关任务修复合同问题。

## 3. 本阶段的文件边界和代码边界

### 3.1 opening build chain 主要边界

主要实现文件：

* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/config/schema.py`
* `configs/bot/phase_b_revalidation_gameplay.yaml`
* `configs/bot/baseline_playable.yaml`（本阶段必须创建并冻结）
* `tests/unit/test_build_progression_contract.py`
* `tests/unit/test_game_loop.py`

职责说明：

* `game_loop.py` 目前是 opening、tech chain、combat-unit production、worker scout、supply sustain、defense execution 的真实主逻辑边界。
* build chain 修复优先在这里做，不要先为了“结构更漂亮”把逻辑打散到多个 manager。
* `schema.py` 是配置字段合法性的真实边界；任何新配置字段必须先在这里落盘。
* `baseline_playable.yaml` 是本阶段正式 gameplay config；`debug.yaml` 不是。

### 3.2 production chain 和 army presence 主要边界

主要实现文件：

* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/managers/macro_manager.py`（仅在确有必要承接 build / production ownership 时修改）
* `src/sc2bot/config/schema.py`
* `tests/unit/test_game_loop.py`
* `tests/unit/test_telemetry_schema.py`

职责说明：

* combat-unit production 的成功不是 `train_command_issued`，而是友军单位真实出现，且 `own_army_count` 或等价证据发生变化。
* rally 只能建立在 army 真实存在之上。

### 3.3 tactical order 和 friendly combat 主要边界

主要实现文件：

* `src/sc2bot/managers/tactical_manager.py`
* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/config/schema.py`
* `tests/unit/test_tactical_manager.py`
* `tests/unit/test_game_loop.py`

职责说明：

* `tactical_manager.py` 负责 rally / defend / attack 计划选择与 combat event 分类。
* `game_loop.py` 负责把战术计划接到真实执行与 telemetry 上。
* 任何 `own_army_count=0` 时发出的 order，都不能作为战术能力证据。

### 3.4 telemetry、evaluation、report 边界

主要文件：

* `evaluation/runner/run_match.py`
* `evaluation/runner/run_batch.py`
* `evaluation/runner/collect_results.py`
* `evaluation/metrics/failure_accounting.py`
* `data/logs/evaluation/...`
* `artifacts/reports/...`

正式 probe / batch config 文件命名必须固定为：

* `configs/evaluation/r1_build_chain_probe.yaml`
* `configs/evaluation/r2_army_presence_probe.yaml`
* `configs/evaluation/r3_tactical_probe.yaml`
* `configs/evaluation/r4_baseline_easy_pool_batch.yaml`
* `configs/evaluation/r4_baseline_confirmation.yaml`

正式 gameplay bot config 文件命名必须固定为：

* `configs/bot/baseline_playable.yaml`

禁止在本阶段使用：

* `configs/bot/debug.yaml` 进行 capability claim
* `configs/bot/opponent_model_*` 进行 playable baseline 验收

## 4. 本阶段的统一证据口径

### 4.1 什么只算代码完成

同时满足以下条件时，才算代码完成：

1. 目标代码已修改并保存；
2. 相关 unit tests 或最小集成测试通过；
3. 配置字段与代码路径一致；
4. 新增 telemetry / event 字段能被静态检查或本地最小运行看到。

代码完成不等于 diagnostic completed。
代码完成更不等于 capability validated。

### 4.2 什么只算 diagnostic completed

以下都只算 diagnostic completed：

1. 看到 `Gateway build command issued`，但没有 ready 证据。
2. 看到 `train_command_issued`，但没有 unit created 或 `own_army_count` 增长。
3. 看到 `army_order`，但 `own_army_count=0`。
4. 看到 `combat_event_detected`，但它只对应 enemy visible，没有友军接敌。
5. 真实运行结束了，但机会窗口不公平或证据缺失。

### 4.3 什么才算 capability validated

同时满足以下条件时，才算 capability validated：

1. 对应 claim 的 prerequisite 已满足；
2. 对应 claim 的机会窗口公平；
3. 证据包完整；
4. 证据不是 command-only；
5. probe / batch 类型与 claim 匹配；
6. 对应 checkpoint 明确接受。

### 4.4 本阶段的证据包最低要求

每次 real probe 或 batch 至少必须有：

1. `summary.json` 或等价 batch 汇总；
2. `match_result.json`；
3. `telemetry/events.jsonl`；
4. `match.SC2Replay`；
5. `replay_metadata.json`；
6. code / config provenance；
7. 本阶段对应报告；
8. queue 中的 `capability_validation_status` 更新。

缺任一关键项时，默认判为 `invalid_evidence`。

### 4.5 统一的 artifact 检查顺序

每次失败先按下面顺序查，不要跳：

1. `docs/plans/active/research_master_task_queue.yaml`
2. `data/logs/evaluation/<run>/summary.json`
3. `data/logs/evaluation/<run>/reallaunch-*/match_result.json`
4. `data/logs/evaluation/<run>/reallaunch-*/telemetry/events.jsonl`
5. `data/logs/evaluation/<run>/reallaunch-*/replay_metadata.json`
6. `data/logs/evaluation/<run>/reallaunch-*/match.SC2Replay`
7. `artifacts/reports/<phase_report>/report.md`

先确认 evidence 是否有效，再判断是不是 gameplay 失败。

## 5. 不能再犯的错误

1. `command telemetry` 不能代替 `structure ready`。
2. `train_command_issued` 不能代替 `combat unit exists`。
3. `own_army_count=0` 时不能声称 `tactical validated`。
4. `enemy combat signal` 不能代替 `friendly combat`。
5. `insufficient_duration` 不能判成 `logic_failure`。
6. `artifact missing` 不能判成 `gameplay failure`。
7. `diagnostic completed` 不能写成 `capability validated`。
8. `debug.yaml` 不能出现在正式 capability 报告里。
9. 不能用扩大样本来掩盖 prerequisite 未满足。
10. 不能在 build chain 未过时跑 army / tactical acceptance。
11. 不能在 baseline 未接受时开始 adaptive 研究。

## 6. 子阶段与 task 映射

本阶段按以下固定顺序执行，不允许跳步：

1. 子阶段 P1：build chain repair 与 build-chain probe

   * `task_004_rebuild_opening_build_chain_logic`
   * `task_005_real_build_chain_probe`
   * `checkpoint_B_build_chain_gate`

2. 子阶段 P2：production chain repair

   * `task_007_rewrite_combat_unit_production_and_rally_logic`

3. 子阶段 P3：army presence validation

   * `task_008_real_army_presence_probe`
   * `checkpoint_C_army_core_gate`

4. 子阶段 P4：tactical order enablement

   * `task_010_rewrite_defend_attack_transition_logic`

5. 子阶段 P5：friendly combat validation

   * `task_011_real_tactical_probe`
   * `checkpoint_D_tactical_core_gate`

6. 子阶段 P6：small eval acceptance

   * `task_013_baseline_easy_pool_batch_evaluation`
   * `task_014_baseline_repair_or_confirmation`
   * `checkpoint_E_level1_baseline_gate`

## 7. 子阶段执行手册

## P1：build chain repair 与 build-chain probe

### 目标

把 opening build progression 从旧 Phase B 的 command-level 诊断状态，推进到可被真实 probe 审核的 capability-level build chain。

### 前置条件

1. `checkpoint_A_start_gate` 已通过。
2. `configs/bot/baseline_playable.yaml` 已由 `task_002` 创建。
3. `baseline_playable.yaml` 的 `runtime.max_game_loop` 已冻结为正式 long-window 值，不能退回 2600。
4. `configs/evaluation/r1_build_chain_probe.yaml` 已存在并指向 `baseline_playable.yaml`。

### 输入

* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/config/schema.py`
* `configs/bot/phase_b_revalidation_gameplay.yaml`
* `configs/bot/baseline_playable.yaml`
* `configs/evaluation/r1_build_chain_probe.yaml`
* `tests/unit/test_build_progression_contract.py`
* `tests/unit/test_game_loop.py`
* 旧 Phase B evidence audit

### 输出

* opening build-chain 修复代码
* `baseline_playable.yaml`
* `r1_build_chain_probe.yaml`
* `artifacts/reports/r1_build_chain_probe/report.md`
* queue 与 handoff 更新

### 执行动作

1. 先确认 `baseline_playable.yaml` 不是从 `debug.yaml` 复制而来，而是从 `phase_b_revalidation_gameplay.yaml` 派生。
2. 在 `game_loop.py` 中确认 opening 行为仍由单一可追踪路径负责；如果需要抽取 helper，只允许抽成 build-chain helper，不允许做大规模架构改写。
3. 确保 Gateway、Assimilator、Cybernetics Core 三段都能输出足以区分以下状态的 telemetry：

   * `attempt`
   * `skipped`
   * `failed`
   * `success`
   * prerequisite / blocker reason
4. 如果没有显式 `Gateway ready` 证据路径，先补证据路径，再跑 probe。允许的 ready 证据来源按优先级排列如下：

   * 显式 ready-count telemetry；
   * 后续 tech 事件中 `gateway_ready_count > 0`；
   * replay 中结构完成，且与 telemetry 时间线一致。
5. 先跑静态 / 单元测试，再跑 real probe。
6. real probe 只回答 build chain 是否成立，不回答 army / tactical / baseline strength。

### minimum gate

1. `Gateway ready` 在有效 real probe 中被验证，或者
2. 在公平机会窗口内，明确给出无歧义 blocker classification。

注意：
“只有 gateway build command”不通过 minimum gate。
“因为 evidence 缺失而看不清 ready”也不通过 minimum gate。

### target gate

1. `Assimilator` 与 `Cybernetics Core` 机会窗口已被公平暴露；
2. 已记录到 `attempt / skip / fail / success` 及原因；
3. 可以清楚区分是 prereq 不满足、duration 不足，还是 logic failure。

### stretch gate

1. 出现 first combat-unit production-ready signal；
2. opening 结构已经可以直接承接 production phase，不需要下一子阶段重写 opening 逻辑。

### 失败分类

* `invalid_evidence`
* `insufficient_duration`
* `missing_prerequisite`
* `build_chain_logic_failure`
* `telemetry_contract_gap`
* `config_drift`

### repair 入口

* 主 repair 入口：`task_004_rebuild_opening_build_chain_logic`
* 如果是 duration / config 合同问题：返回 `task_002_lock_runtime_eval_contract_and_config_roles`
* 如果只是证据缺失：原样 rerun `task_005_real_build_chain_probe`

### 不能做什么

1. 不能在 P1 报告里写 army 已成立。
2. 不能用 command-only telemetry 通过 P1。
3. 不能把 P1 的 run 拿去写 tactical 结论。
4. 不能用 short-window 或 debug config 补跑。

### 不允许进入 P2 的条件

任一条件出现都不得进入 P2：

1. `checkpoint_B_build_chain_gate` 未通过；
2. `Gateway ready` 未被验证且 blocker 不清楚；
3. `actual_game_time_sufficient = no`；
4. `baseline_playable.yaml` 仍不稳定；
5. 证据包不完整。

## P2：production chain repair

### 目标

让 combat-unit production、continued production、rally eligibility 在代码与 telemetry 上都可追踪，并为真实 army validation 提供稳定前提。

### 前置条件

1. `checkpoint_B_build_chain_gate` 已通过。
2. opening build chain 已具备向 production 推进的前提。
3. `baseline_playable.yaml` 已冻结 build-chain 相关字段，避免 P2 一边修生产一边漂移 opening。

### 输入

* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/managers/macro_manager.py`（仅在 build / production ownership 需要收敛时使用）
* `src/sc2bot/managers/tactical_manager.py`（仅用于 rally eligibility，不用于战术验收）
* `src/sc2bot/config/schema.py`
* `configs/bot/baseline_playable.yaml`
* `tests/unit/test_game_loop.py`
* `tests/unit/test_telemetry_schema.py`

### 输出

* combat-unit production 修复代码
* rally eligibility 修复代码
* production telemetry 完整化
* army probe 所需配置和测试准备

### 执行动作

1. 明确 `combat-unit production` 的成功定义是“单位真实出现”，不是“发出 train 命令”。
2. 在 `game_loop.py` 中整理 `_safe_combat_unit_production` 相关前提判断，至少要能区分：

   * `gateway_ready_count`
   * `cybernetics_core_ready_count`
   * `idle_gateway_count`
   * affordability
   * unsupported unit name
3. 确保 `own_army_count` 的提取和落盘是可检查的；如果 state extraction 不可信，先修 extraction，不得直接跑 P3。
4. rally 逻辑只能在 `own_army_count > 0` 或等价单位存在条件下进入“可执行”状态。
5. 只修 production 与 rally prerequisite，不要提前写 defend / attack success。

### minimum gate

1. 代码层面能明确区分 `train_command_issued` 与 `unit exists`；
2. `own_army_count` 或等价 army existence 证据路径已存在；
3. rally eligibility 不会在无 army 时误触发。

### target gate

1. continued production 有显式可追踪路径；
2. 第一支 army 出现后，rally 不再依赖偶发副作用；
3. production failure 可以明确指向 supply、gas、idle gateway 或 tech prerequisite。

### stretch gate

1. production path 已能支撑简单的 zealot / stalker 分流；
2. 下一子阶段只需要 real validation，不需要再重写生产主链。

### 失败分类

* `production_logic_failure`
* `state_extraction_failure`
* `supply_block_unhandled`
* `tech_prerequisite_regression`
* `config_drift`

### repair 入口

* 主 repair 入口：`task_007_rewrite_combat_unit_production_and_rally_logic`
* 如果 opening 回归：返回 P1 / `task_004`
* 如果只是 tests 不足：先补 tests，再不允许进入 P3

### 不能做什么

1. 不能在 P2 结束时声称 army validated。
2. 不能因为看到 `train_command_issued` 就判定 production 成立。
3. 不能把 rally 日志当 army existence 证据。
4. 不能在这个子阶段引入 adaptive gating。

### 不允许进入 P3 的条件

1. `unit exists` 与 `train command` 仍无法区分；
2. `own_army_count` 证据路径不可信；
3. rally 仍会在 `own_army_count=0` 时触发；
4. opening build-chain 被回归破坏。

## P3：army presence validation

### 目标

在真实 SC2 中确认友军 army 真实出现，而不是停留在 production 命令层。

### 前置条件

1. P2 minimum gate 与 target gate 已满足。
2. `configs/evaluation/r2_army_presence_probe.yaml` 已创建并指向 `baseline_playable.yaml`。
3. P1 build-chain 结果仍然有效。

### 输入

* `configs/bot/baseline_playable.yaml`
* `configs/evaluation/r2_army_presence_probe.yaml`
* `src/sc2bot/runtime/game_loop.py`
* `data/logs/evaluation/...`
* `artifacts/reports/r2_army_presence_probe/report.md`

### 输出

* real army probe artifacts
* army presence 报告
* `checkpoint_C_army_core_gate` 所需 evidence

### 执行动作

1. 使用 `baseline_playable.yaml` 跑 real army presence probe。
2. 重点检查以下证据链：

   * combat-unit production event
   * `own_army_count` 变化
   * replay 中实际单位出现
   * rally event 是否建立在真实 army 之上
3. 若 `own_army_count` 仍为 0，先判断是 production 没成功、state extraction 错、还是 run 无效，不要直接判 tactical 失败。
4. 只有在 evidence 完整、duration 充分的前提下，才允许判断 army presence 是否成立。

### minimum gate

1. 有效 real probe 中 `own_army_count > 0`；
2. replay 中可复核友军战斗单位出现；
3. `match_result.json`、`events.jsonl`、replay、provenance 完整。

### target gate

1. army presence 不是一次性偶发；
2. 至少存在最小必要 rerun 或同类证据，表明第一支 army 的出现可复现；
3. rally 行为建立在真实 army 之上。

### stretch gate

1. 第一支 army 之后出现受控移动；
2. production 没有立刻塌回 `own_army_count=0` 的伪稳定态。

### 失败分类

* `invalid_evidence`
* `insufficient_duration`
* `missing_prerequisite`
* `production_logic_failure`
* `state_extraction_failure`
* `army_transient_only`

### repair 入口

* 主 repair 入口：`task_007_rewrite_combat_unit_production_and_rally_logic`
* 若 build chain 回归：返回 P1 / `task_004`
* 若只是 evidence invalid：rerun `task_008_real_army_presence_probe`

### 不能做什么

1. 不能因为有 rally event 就写 army 已存在。
2. 不能因为某个单位短暂出现一帧就夸大为 army core 稳定成立。
3. 不能跳过 `checkpoint_C_army_core_gate` 直接做 tactical 结论。

### 不允许进入 P4 的条件

1. `checkpoint_C_army_core_gate` 未通过；
2. `own_army_count > 0` 没被真实验证；
3. rally 仍不能与真实 army 绑定；
4. army 只在无效证据里出现。

## P4：tactical order enablement

### 目标

让 defend / attack / rally 的触发逻辑建立在真实 army 和真实前置之上，而不是仅在 telemetry 中看起来发生了。

### 前置条件

1. `checkpoint_C_army_core_gate` 已通过。
2. 友军 army 已被真实验证。
3. `tactical_manager.py` 的现有逻辑已被审查，明确知道当前哪些路径会产生假 order。

### 输入

* `src/sc2bot/managers/tactical_manager.py`
* `src/sc2bot/runtime/game_loop.py`
* `src/sc2bot/config/schema.py`
* `configs/bot/baseline_playable.yaml`
* `tests/unit/test_tactical_manager.py`
* `tests/unit/test_game_loop.py`

### 输出

* defend / attack / rally 逻辑修复
* tactical reason 字段完善
* 真实 tactical probe 准备完成

### 执行动作

1. 把 defend / attack / rally 的合法触发条件写清楚：

   * `own_army_count > 0`
   * attack 只在 army / time / enemy location 前置满足时允许
   * defend 只在有威胁上下文时允许
2. 在 `tactical_manager.py` 中显式输出 `reason`，不得只输出 order 类型。
3. 在 `game_loop.py` 中确保 `army_order` 与 tactical reason 被真实落盘。
4. 若当前逻辑会在 `own_army_count=0` 时生成 `attack_order` 或 `defend_order`，必须先修完再进入 P5。

### minimum gate

1. 静态和最小集成测试表明无 army 时不会出合法 tactical order；
2. tactical reason 字段完整；
3. rally / defend / attack 三类计划至少有明确可区分输出。

### target gate

1. tactic plan 能把 army 从“存在”推进到“受控移动”；
2. 攻防切换不再只依赖单个 if/else 的偶然命中；
3. 下一个 real tactical probe 能明确回答“为什么没打起来”。

### stretch gate

1. regroup / fallback 原因也已准备好；
2. P5 失败时可以直接归因，不需要回头补 telemetry。

### 失败分类

* `tactical_logic_failure`
* `reason_field_missing`
* `army_prerequisite_regression`
* `config_threshold_mismatch`

### repair 入口

* 主 repair 入口：`task_010_rewrite_defend_attack_transition_logic`
* 若 army prerequisite 回归：返回 P2 / `task_007`

### 不能做什么

1. 不能在 P4 静态完成后声称 tactical validated。
2. 不能用 `enemy visible` 替代合法 defend。
3. 不能在本子阶段偷偷改 baseline 的 build / production 主逻辑。

### 不允许进入 P5 的条件

1. `own_army_count=0` 时仍可能出 tactical order；
2. tactical reason 不完整；
3. 当前逻辑无法区分“无威胁”和“有威胁但无 army”；
4. attack / defend 仍依赖隐式副作用。

## P5：friendly combat validation

### 目标

在真实 SC2 中验证合法 tactical order 和 friendly combat，不再只剩 enemy-visible signal。

### 前置条件

1. P4 minimum 和 target 已满足。
2. `configs/evaluation/r3_tactical_probe.yaml` 已创建。
3. army presence 仍然稳定，不存在新回归。

### 输入

* `configs/bot/baseline_playable.yaml`
* `configs/evaluation/r3_tactical_probe.yaml`
* `src/sc2bot/managers/tactical_manager.py`
* `src/sc2bot/runtime/game_loop.py`
* tactical probe artifacts

### 输出

* `r3_tactical_probe` artifacts
* `artifacts/reports/r3_tactical_probe/report.md`
* `checkpoint_D_tactical_core_gate` 所需 evidence

### 执行动作

1. 跑 real tactical probe。
2. 检查以下证据链是否闭环：

   * `army_order`
   * `own_army_count`
   * target / reason
   * `combat_event_detected` 或等价事件
   * replay 中友军接敌
3. 如果只有 `enemy combat signal`，先判断是否没有友军 army、没有合法 order、还是接敌位置 / 时机问题。
4. 没有 friendly combat 时，默认不能进入 P6；只有 `checkpoint_D` 明确写出“允许以近邻形态进入 P6”时，才允许例外放行。

### minimum gate

1. 至少一种合法 tactical order 在真实对局中成立；
2. 该 order 发生时 `own_army_count > 0`；
3. 证据包完整。

### target gate

1. `friendly combat` 被真实验证；
2. replay 与 telemetry 一致表明友军 army 参与接敌；
3. 不再依赖 enemy-visible 作为主要战斗结论。

### stretch gate

1. defend 与 attack 两种行为都能在有效窗口中观察到；
2. 若只观察到一种行为，报告中必须写出另一种行为缺失的原因和 repair 入口。

### 失败分类

* `invalid_evidence`
* `insufficient_duration`
* `missing_prerequisite`
* `tactical_logic_failure`
* `no_contact_under_valid_conditions`
* `enemy_only_combat_signal`
* `army_regression`

### repair 入口

* 主 repair 入口：`task_010_rewrite_defend_attack_transition_logic`
* 若 army 回归：返回 P2 / `task_007`
* 若仅证据缺失：rerun `task_011_real_tactical_probe`

### 不能做什么

1. 不能把 `enemy_only_combat_signal` 写成 `friendly combat validated`。
2. 不能因为看到了 attack tag 就写战术成功。
3. 不能跳过 `checkpoint_D_tactical_core_gate` 进入 baseline batch。

### 不允许进入 P6 的条件

1. `checkpoint_D_tactical_core_gate` 未通过；
2. 合法 tactical order 未验证；
3. friendly combat 仍完全缺失，且无明确 checkpoint 豁免说明；
4. army prerequisite 回归。

## P6：small eval acceptance

### 目标

证明 `baseline_playable` 已经不再是 survival scaffold，而是可被真实 batch 审核的 Level 1 playable baseline。

### 前置条件

1. `checkpoint_D_tactical_core_gate` 已通过。
2. `configs/maps/baseline_easy_pool_maps.yaml` 已从现有 easy map slice 冻结出来。
3. `configs/opponents/baseline_easy_pool.yaml` 已从现有 easy opponent slice 冻结出来。
4. `configs/evaluation/r4_baseline_easy_pool_batch.yaml` 与 `configs/evaluation/r4_baseline_confirmation.yaml` 已创建。
5. baseline build / production / tactical 主逻辑版本冻结，不允许 batch 中途继续漂移。

### 输入

* `configs/bot/baseline_playable.yaml`
* `configs/maps/baseline_easy_pool_maps.yaml`
* `configs/opponents/baseline_easy_pool.yaml`
* `configs/evaluation/r4_baseline_easy_pool_batch.yaml`
* `configs/evaluation/r4_baseline_confirmation.yaml`
* `evaluation/runner/run_batch.py`
* `evaluation/metrics/failure_accounting.py`

### 输出

* baseline batch artifacts
* confirmation / repair artifacts
* `artifacts/reports/r4_baseline_easy_pool/report.md`
* `artifacts/reports/r4_baseline_repair_or_confirmation/report.md`
* `checkpoint_E_level1_baseline_gate` 所需 evidence

### 执行动作

1. 用 frozen easy slice 跑正式 baseline batch。
2. 报告中必须把以下三类内容分开写：

   * infrastructure 是否正常；
   * gameplay capability 是否成立；
   * research contribution 是否不适用。
3. batch 结束后，先做 dominant failure class 排序，再决定是进入一次 focused repair 还是 confirmation rerun。
4. 若 target 已经通过，只允许做最小 confirmation，不允许扩大 scope。
5. 若 target 未通过，只能修 dominant failure class，不允许同时修多个方向。

### minimum gate

1. batch 中不存在系统性 prerequisite regression；
2. bot 已经不只是诊断体；
3. 至少出现一场无争议的真正胜利，或同强度的极强 near-win，并且有完整 gameplay evidence 支撑。

### target gate

1. easy slice 上出现重复性 outcome 证据；
2. outcome 与 gameplay evidence 一致；
3. baseline 已可作为后续 adaptive paired evaluation 的 control。

### stretch gate

1. medium slice 或更难切片出现非退化对局；
2. dominant failure class 收敛为少数明确问题，而非系统性混乱。

### 失败分类

* `invalid_evidence`
* `diagnostic_only_batch`
* `build_chain_regression`
* `production_regression`
* `tactical_regression`
* `stability_failure`
* `confirmation_conflict`

### repair 入口

* 轻微不稳定：`task_014_baseline_repair_or_confirmation`
* tactical regression：返回 P4 / `task_010`
* army / production regression：返回 P2 / `task_007`
* build-chain regression：返回 P1 / `task_004`

### 不能做什么

1. 不能在 P6 才开始补 prerequisite。
2. 不能把 small eval 的存在当成 accepted baseline。
3. 不能扩大对手池来掩盖 easy slice 未通过。
4. 不能在 baseline batch 中混入 adaptive 逻辑。
5. 不能把单局亮点写成 batch 结论。

### 不允许离开本阶段的条件

1. `checkpoint_E_level1_baseline_gate` 未通过；
2. batch 仍以 diagnostic-only 为主；
3. dominant failure class 未处理；
4. baseline control 版本仍在漂移。

## 8. 本阶段的 release 规则

只有满足以下条件，才允许离开 playable core rebuild 阶段：

1. P1 到 P6 对应 checkpoint 全部通过；
2. `baseline_playable.yaml` 已冻结为 accepted control；
3. Level 1 baseline 的结论来自 real batch，而不是单 probe；
4. 所有 claim 都已在 queue 中被标成正确的 `capability_validation_status`；
5. `docs/handoffs/latest.md` 已明确下一阶段是 `phase_adaptive_response_research`，而不是继续补 playable baseline 的未完成项。

本阶段结束后，项目才允许进入 research contribution 阶段。
在此之前，任何 opponent-model、belief-state、adaptive response 的工作都不得进入 mainline claim。
