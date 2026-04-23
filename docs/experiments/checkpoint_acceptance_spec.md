
# Checkpoint Acceptance Specification

状态：active
更新日期：2026-04-23
适用范围：所有 `research_master_task_queue.yaml` 中的 checkpoint 任务
直接依赖：

* `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
* `docs/plans/active/research_master_task_queue.yaml`
* `docs/experiments/real_match_validation_protocol.md`

## 1. checkpoint 的职责

checkpoint 不是总结会，也不是写报告的形式动作。
checkpoint 的职责只有三个：

1. 审核前几个任务是否真正达到计划目标；
2. 严格区分 `task completed`、`diagnostic completed`、`capability validated`；
3. 决定是否允许进入后续任务。

checkpoint 不能做的事：

1. 不能替代 real evidence；
2. 不能替代 phase gate；
3. 不能因为“看起来差不多”而放行；
4. 不能为缺失的 evidence 补写成功叙述。

## 2. 什么时候必须 checkpoint

### 2.1 固定规则

每 3 个任务必须有一个 checkpoint。

默认结构是：

1. 实现 / 修复任务
2. 真实验证任务
3. checkpoint 任务

不允许把第 3 个 checkpoint 省略掉。

### 2.2 天然必须 checkpoint 的任务组

以下任务组天然需要 checkpoint：

1. build chain repair -> build-chain probe -> build-chain checkpoint
2. production repair -> army probe -> army checkpoint
3. tactical repair -> tactical probe -> tactical checkpoint
4. baseline batch -> repair / confirmation -> baseline checkpoint
5. adaptive gate integration -> paired evaluation -> research checkpoint

### 2.3 为什么 checkpoint 不能省略

因为前两个任务最多只能说明：

* 代码改了；
* 跑过了；
* 有一些信号了。

只有 checkpoint 才负责回答：

* minimum gate 到底过没过；
* target gate 到底过没过；
* 这次证据是 capability validated 还是 diagnostic only；
* 下一步到底是继续、repair、重做还是回退。

## 3. checkpoint 的输入

每次 checkpoint 必须读取以下输入，缺一不可：

1. 当前 checkpoint 的 `reviewed_tasks`
2. 每个 reviewed task 的 queue 条目
3. reviewed task 对应的 code / config provenance
4. reviewed task 对应的 real artifacts
5. 对应 phase 报告
6. 对应 phase 的 minimum / target / stretch gate 定义
7. `real_match_validation_protocol.md`
8. 相关 prior checkpoint 结论

如果输入不全，checkpoint 默认不能放行。

## 4. checkpoint 输出的固定字段

每个 checkpoint 任务必须写出以下固定字段，不允许删减：

1. `reviewed_tasks`
2. `evidence_paths`
3. `minimum_gate_passed`
4. `target_gate_passed`
5. `stretch_gate_status`
6. `actual_game_time_sufficient`
7. `capability_validation_status`
8. `failure_class`
9. `decision`
10. `next_allowed_task`

## 5. 每个字段的定义

### 5.1 `reviewed_tasks`

定义：
本次 checkpoint 真正审核的任务列表。

要求：

1. 必须与 queue 中 `requires` 对齐；
2. 不允许漏掉关键前置任务；
3. 不允许把未完成任务写进来冒充已审核。

### 5.2 `evidence_paths`

定义：
支持本次 checkpoint 结论的真实文件路径列表。

要求：

1. 必须指向具体 artifact、report 或 queue 记录；
2. 不能只写目录名而没有可追溯文件；
3. 如果 evidence path 为空，checkpoint 默认不通过。

推荐最小集合：

* `data/logs/evaluation/.../summary.json`
* `data/logs/evaluation/.../reallaunch-*/match_result.json`
* `data/logs/evaluation/.../reallaunch-*/telemetry/events.jsonl`
* `data/logs/evaluation/.../reallaunch-*/match.SC2Replay`
* `artifacts/reports/<phase>/report.md`
* `artifacts/reports/checkpoints/<checkpoint_id>.md`

### 5.3 `minimum_gate_passed`

允许值：

* `true`
* `false`

含义：
是否具备进入下一阶段的最低资格。

判定规则：

1. prerequisite 满足；
2. evidence 有效；
3. 机会窗口公平；
4. claim 与验证单元匹配；
5. reviewed_tasks 至少达到 minimum gate。

少一项都不能写 `true`。

### 5.4 `target_gate_passed`

允许值：

* `true`
* `false`

含义：
该 phase 是否真正达到设计目标。

注意：
`minimum_gate_passed = true` 不自动推出 `target_gate_passed = true`。

### 5.5 `stretch_gate_status`

允许值：

* `passed`
* `failed`
* `not_attempted`
* `pending`

含义：
stretch 是否达到，是否给后续阶段带来额外低风险起点。

### 5.6 `actual_game_time_sufficient`

允许值：

* `yes`
* `no`
* `not_applicable`
* `ambiguous`

定义：
reviewed evidence 是否在与 claim 对应的公平机会窗口内完成。

判定规则：

1. 对静态 / 文档任务：`not_applicable`
2. 对 probe：

   * 若有效 run 已达到该 claim 的最小公平机会窗口，写 `yes`
   * 若在窗口前结束，写 `no`
3. 对 batch：

   * 若所有 load-bearing runs 都足够，写 `yes`
   * 若任一 load-bearing run 不足够，写 `no`
4. 对 paired evaluation：

   * 只有 control / treatment 双侧都足够，才写 `yes`
   * 只要一侧不足，写 `no`
5. 若 evidence 混乱、无法判定，写 `ambiguous`

`actual_game_time_sufficient = no` 时，不允许把结果写成 gameplay failure，除非另有独立逻辑证据。

### 5.7 `capability_validation_status`

允许值建议固定为：

* `not_applicable`
* `task_completed_only`
* `diagnostic_completed`
* `capability_validated_minimum`
* `capability_validated_target`
* `invalid_evidence`
* `blocked_pending_prerequisite`

含义：
本次 checkpoint 对 reviewed tasks 能给出的最高能力判定级别。

### 5.8 `failure_class`

定义：
本次 checkpoint 识别出的主导失败类型。

允许使用的主类：

* `none`
* `invalid_evidence`
* `insufficient_duration`
* `missing_prerequisite`
* `logic_failure`
* `stability_failure`
* `regression`
* `no_behavior_change`
* `no_causal_benefit`
* `scope_mixed_needs_split`

要求：

1. 必须是主导失败；
2. 不允许写成模糊描述，如“还需要优化”；
3. 如果没有失败，写 `none`。

### 5.9 `decision`

允许值固定为：

* `accepted_continue`
* `repair_and_rerun`
* `rework_required`
* `blocked`
* `split_required`
* `return_to_prior_phase`

禁止出现任何自由文本 decision。

### 5.10 `next_allowed_task`

定义：
checkpoint 后唯一允许执行的下一个 queue task 或分支映射。

要求：

1. 必须具体到 task id；
2. 若存在多条失败路径，必须显式写成分支映射；
3. 不允许写“继续看看”；
4. 如果 decision 不是 `accepted_continue`，`next_allowed_task` 必须指向 repair、rerun、split 或 prior phase 任务。

## 6. decision 的精确定义

### 6.1 `accepted_continue`

只在以下条件同时满足时允许：

1. `minimum_gate_passed = true`
2. reviewed evidence 有效
3. 当前 phase 的 prerequisite 没有回归
4. queue 中没有更早 blocked 的前序问题

含义：
允许进入下一阶段。

### 6.2 `repair_and_rerun`

适用条件：

1. 失败类型明确；
2. repair 范围可控；
3. 仍在当前 phase 内解决最合理。

含义：
先修 dominant failure，再回原验证单元。

### 6.3 `rework_required`

适用条件：

1. 任务看似完成，但产物不符合计划目标；
2. 代码边界、配置边界或报告结构需要重做；
3. 当前任务没有形成可接受的输入给下一任务。

含义：
当前任务本身必须重做，不能简单 rerun。

### 6.4 `blocked`

适用条件：

1. evidence 无效；
2. prerequisite 未满足；
3. actual game time 不足；
4. reviewed_tasks 本身缺失关键输入。

含义：
不得继续执行后续阶段。

### 6.5 `split_required`

适用条件：

1. 一个任务里混入了实现、真实评测、报告三件事；
2. 根因不清，需要先拆出 debug task；
3. reviewed evidence 无法支持单一 decision。

含义：
先拆任务，再执行。

### 6.6 `return_to_prior_phase`

适用条件：

1. 发现前一 phase 的 prerequisite 回归；
2. 当前 phase 的失败实际上来自更早 phase；
3. 若继续当前 phase，只会产出更多 diagnostic-only。

含义：
显式回到 prior phase，不允许留在当前 phase 硬跑。

## 7. checkpoint 的判定流程

每次 checkpoint 必须按以下顺序判断，不允许跳步骤：

1. 确认 `reviewed_tasks` 是否全部处于可审核状态；
2. 确认 evidence package 是否完整；
3. 判断 `actual_game_time_sufficient`；
4. 判断 prerequisite 是否满足；
5. 判断 reviewed tasks 只到 `task completed`、`diagnostic completed` 还是 `capability validated`；
6. 逐一比较 minimum / target / stretch gate；
7. 确定 `failure_class`；
8. 确定 `decision`；
9. 写出 `next_allowed_task`；
10. 更新 queue 和 checkpoint report。

若第 2 步失败，则后面不能直接判 gameplay failure。
若第 3 步失败，则后面不能把结果写成 logic failure。
若第 4 步失败，则后面不能放行。

## 8. 什么情况下 minimum gate 算通过

minimum gate 同时满足以下条件才算通过：

1. 当前 checkpoint 的关键 prerequisite 已满足；
2. reviewed evidence 完整且有效；
3. 对应 claim 的验证单元正确；
4. reviewed tasks 至少完成 phase 的最低能力目标；
5. 不存在把 diagnostic 当 capability 的偷换。

示例：

* build-chain checkpoint：只有看到 gateway command，不算 minimum 通过；
* army checkpoint：没有 `own_army_count > 0`，minimum 不通过；
* tactical checkpoint：只有 enemy visible，没有合法 own-army order，minimum 不通过；
* adaptive checkpoint：只有 tag 改变，没有 behavior delta，minimum 不通过。

## 9. 什么情况下 target gate 算通过

target gate 通过要求：

1. minimum 已通过；
2. 当前 phase 的核心目标已经被直接证据支持；
3. 不需要再靠“解释性文字”补逻辑；
4. 下一阶段能在不返工当前主链的情况下开始。

target 通过不要求 stretch 一定通过。

## 10. 什么情况下只能判 diagnostic completed

出现以下任一情形时，只能判 `diagnostic_completed`：

1. 只有 command telemetry；
2. `own_army_count=0` 时出现 tactical signal；
3. `friendly combat` 缺失，只剩 `enemy visible`；
4. actual game time 不足，但仍有一些中间信号；
5. telemetry 存在，但与 replay / result 对不上；
6. behavior tag 改了，但 paired behavior 没变。

## 11. 什么情况下必须拦截后续阶段

出现以下任一情形时，checkpoint 必须拦截：

1. `minimum_gate_passed = false`
2. `actual_game_time_sufficient = no`
3. `capability_validation_status = invalid_evidence`
4. prerequisite regression
5. reviewed task scope 混乱，需要拆分
6. baseline 未接受，却试图进入 adaptive phase
7. control / treatment 不可比，却试图宣称 research 结论

## 12. checkpoint 的常见错误

以下错误必须在 checkpoint 审核时主动防止：

1. 只看 task status，不看 evidence。
2. 只看 telemetry 是否存在，不看它证明了什么。
3. 只看单次 run，却在做 batch / paired claim。
4. 忽略 opportunity window。
5. 忽略 `own_army_count` prerequisite。
6. 忽略 friendly combat prerequisite。
7. 用报告 closeout 语言替代 gate 判断。
8. 发现 evidence 缺失后仍继续做逻辑结论。
9. 不写 `failure_class`，导致下一步 repair 无入口。
10. checkpoint 明知 minimum 未过，却仍把后续任务保持为可执行。

## 13. checkpoint report 的文件要求

每次 checkpoint 除了更新 queue，还必须写单独报告：

* `artifacts/reports/checkpoints/<checkpoint_id>.md`

该报告至少包含：

1. reviewed tasks 概览
2. evidence package 完整性检查
3. actual game time sufficiency 判定
4. minimum / target / stretch 判定
5. capability_validation_status
6. failure_class
7. decision
8. next_allowed_task

checkpoint 报告与 queue 字段必须一致。
若两者冲突，以更保守的结论为准，并立即修正冲突。

## 14. checkpoint 的最终原则

checkpoint 只做一件事：
把“执行过了”变成“是否真的被接受”。

如果 evidence 不能支持 acceptance，checkpoint 就必须拦。
如果 prerequisite 未满足，checkpoint 就必须退。
如果根因不清，checkpoint 就必须拆。
如果 minimum 没过，checkpoint 就不能放行。
