
# Codex Execution Rules Research Mode

状态：active
更新日期：2026-04-23
适用对象：在本仓库内执行 mainline 任务的 Codex
直接依赖：

* `docs/plans/active/research_master_task_queue.yaml`
* `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
* `docs/experiments/real_match_validation_protocol.md`
* `docs/experiments/checkpoint_acceptance_spec.md`

## 1. 总原则

Codex 在 research mode 下不是自由探索者，而是受 queue 和 checkpoint 约束的执行器。

Codex 的首要责任不是“多做事”，而是：

1. 按正确顺序做正确的事；
2. 不把 diagnostic 写成 validated；
3. 不在错误阶段消耗真实 SC2 预算；
4. 不在 checkpoint 未通过时擅自推进。

## 2. 每轮执行的固定起始动作

每一轮开始时，Codex 必须按以下顺序执行：

1. 打开 `docs/plans/active/research_master_task_queue.yaml`
2. 确认 `active_next_task`
3. 读取该 task 的：

   * `requires`
   * `status`
   * `validation_level_required`
   * `quota_risk`
   * `data_source`
   * `real_validation_status`
4. 确认最近一个 checkpoint 的 `decision`
5. 确认本轮任务是否允许跑真实 SC2
6. 确认是否存在 blocked prerequisite
7. 确认本轮任务是否超出单轮可控范围

如果以上任一项没有确认，本轮不得动手改代码或跑评测。

## 3. 一次只做一个任务

默认规则：

* 一次只做一个 queue task。

例外规则：

* paired evaluation 任务本身可以包含 control / treatment 两个 sibling runs，但它们仍属于同一个 queue task。
* checkpoint 任务可以读取多个 reviewed task，但它本身仍是一个 queue task。

禁止做法：

1. 同轮同时推进两个 pending task。
2. 一边修当前任务，一边提前做下一个任务的 real eval。
3. 在 queue 未授权时，顺手补 unrelated docs / research prototype。

## 4. Codex 每轮必须确认的四件事

### 4.1 `requires` 是否满足

只要有一个 `requires` 未满足，就必须停。

### 4.2 `validation_level_required` 是否匹配

* 需要 L1 的任务，不要跑真实 SC2 冒充完成；
* 需要 L3 / L4 的任务，不要只写代码或报告就标完成；
* 需要 L5 的 checkpoint，不要只写一句“通过”。

### 4.3 本轮是否允许跑真实 SC2

必须同时满足：

1. 该任务的验证级别要求真实 SC2；
2. `real_match_validation_protocol.md` 允许此类任务在当前阶段跑真实 SC2；
3. prerequisite 已满足；
4. 当前没有 blocked checkpoint。

### 4.4 本轮是否会造成 scope 膨胀

如果一个任务同时混有：

1. 代码实现；
2. 真实评测；
3. 报告 / queue / handoff 更新；

并且根因还不清楚，则必须先拆，不得直接一口气做完。

## 5. Codex 做完任务后必须更新的内容

每轮任务结束后，Codex 必须更新：

1. `docs/plans/active/research_master_task_queue.yaml`
2. `docs/handoffs/latest.md`
3. 本任务对应的 phase report
4. 若是 real eval，还要确认 artifact 路径已落盘

queue 至少要更新的字段：

1. `status`
2. `actual_validation_level`
3. `real_validation_status`
4. `evidence_paths`
5. `capability_validation_status`

如果是 checkpoint，还必须更新：

1. `reviewed_tasks`
2. `minimum_gate_passed`
3. `target_gate_passed`
4. `stretch_gate_status`
5. `actual_game_time_sufficient`
6. `failure_class`
7. `decision`
8. `next_allowed_task`

如果没有完成这些更新，本轮任务不能算完成。

## 6. Codex 不允许做的事情

1. 不允许跳过 queue task。
2. 不允许擅自改 `active_next_task` 指向下一个阶段。
3. 不允许把 `diagnostic_completed` 写成 `capability_validated`。
4. 不允许因为“看起来差不多”就把 task 标 `completed`。
5. 不允许在 checkpoint 未通过时继续执行后续 task。
6. 不允许擅自扩大任务范围。
7. 不允许把 `research/` 目录里的 prototype 拖进 mainline。
8. 不允许用 `debug.yaml` 做 capability claim。
9. 不允许在 baseline 未冻结时做 adaptive paired eval。
10. 不允许在 paired eval 中同时改 control 和 treatment 的 baseline core。
11. 不允许用更大的 batch 掩盖 prerequisite 未满足。
12. 不允许跳过 handoff 更新。
13. 不允许把 artifact 缺失的 run 当证据使用。
14. 不允许为了节省时间而省略 checkpoint。

## 7. Codex 在什么情况下必须停

出现以下任一情况时，Codex 必须 stop，而不是继续：

1. `requires` 未满足；
2. 最近 checkpoint 的 `decision` 不是 `accepted_continue`；
3. 当前任务需要 real SC2，但协议不允许；
4. evidence 不够；
5. probe 跑完仍无法判定；
6. 机会窗口不足；
7. replay / result / telemetry 缺失；
8. scope 已经膨胀到单轮不可控；
9. 当前任务 `quota_risk = high`，且根因不清；
10. control / treatment 不可比；
11. 当前问题明显来自 prior phase。

stop 后允许的动作只有：

1. 更新 queue 为 blocked / split_required / return_to_prior_phase；
2. 写 handoff；
3. 创建或指向 repair / rerun / split 入口。

stop 后不允许继续改 unrelated 代码。

## 8. Codex 在什么情况下必须 split task

出现以下任一情形，Codex 必须拆任务：

1. 一个任务会超出单轮可控额度；
2. 一个任务里混了实现、真实评测、报告三种事情；
3. 根因不明确，需要先做 debug / evidence triage；
4. 当前 task 的 real eval 要求依赖尚未冻结的 config；
5. paired eval 还没完成 control / treatment contract 冻结；
6. 当前 task 实际上包含两个不同 failure class。

split 的结果应写成：

1. queue 中的 `decision: split_required`
2. `failure_class: scope_mixed_needs_split`
3. `next_allowed_task` 指向更小的 repair / debug / contract task

没有 split，就不能继续执行混合任务。

## 9. Codex 在什么情况下必须 rerun

出现以下任一情况，Codex 必须 rerun 同级验证单元，而不是直接改代码：

1. `invalid_evidence`
2. artifact 不完整
3. paired run 中一侧缺失
4. actual game time 不足，但逻辑尚未被公平暴露
5. config 漂移导致本次 run 不可比
6. control / treatment 不可比
7. summary / replay / telemetry 之间记录冲突
8. report 结论与 raw evidence 不一致

rerun 时必须保持：

1. claim 不变；
2. 主逻辑版本不变；
3. 修复仅限 evidence / contract；
4. rerun 原因写入 handoff 和 report。

## 10. Codex 在什么情况下必须创建 repair task

出现以下任一情况，Codex 必须进入或创建 repair 路径：

1. Gateway ready 一直不成立；
2. Cyber Core 不出现；
3. Zealot / Stalker 不出现；
4. `own_army_count` 一直为 0；
5. attack / defend 从未发生；
6. 只有 enemy combat signal，没有 friendly combat；
7. small eval 全是 diagnostic；
8. adaptive 只改 telemetry，不改行为；
9. paired A/B 没有真实差异；
10. 当前 failure class 明确，且 rerun 不会产生新信息。

repair task 必须满足：

1. 只修一个 dominant failure class；
2. 修完后必须 rerun 相应 probe / batch；
3. 不得偷偷扩大为新 feature；
4. 必须更新 queue 的 `failure_class` 和 `next_allowed_task`。

## 11. Codex 在什么情况下必须 return_to_prior_phase

出现以下任一情况，Codex 必须回到 prior phase：

1. build-chain regression 出现在 army / tactical 阶段；
2. army prerequisite regression 出现在 tactical / batch 阶段；
3. baseline core regression 出现在 adaptive 阶段；
4. 当前 phase 的 failure 实际来自更早 phase；
5. 继续当前 phase 只会得到更多 diagnostic-only。

回退时必须显式写：

1. `decision: return_to_prior_phase`
2. `next_allowed_task` 指向 prior phase repair task
3. `docs/handoffs/latest.md` 中写明回退原因

## 12. Codex 的 real-match 纪律

任何 real-match task 开始前，Codex 必须确认：

1. `bot_config` 指向正式 config，而不是 `debug.yaml`
2. `evaluation config` 指向正确的 output_dir
3. map / opponent slice 与当前 claim 匹配
4. evidence 落盘路径明确
5. 若是 paired eval，control / treatment 路径成对明确

任何 real-match task 结束后，Codex 必须确认：

1. `summary.json` 存在
2. `match_result.json` 存在
3. `telemetry/events.jsonl` 存在
4. `match.SC2Replay` 存在
5. provenance 可追溯
6. 结果已写回 report / queue / handoff

## 13. Codex 的状态标记纪律

### `completed`

只能表示：
任务动作完成。

不能表示：
能力已验证。

### `diagnostic_completed`

只能表示：
任务跑出了有价值的中间信号或 blocker 分类。

不能表示：
minimum gate 已过。

### `capability_validated`

只能在以下条件同时满足时使用：

1. prerequisite 满足；
2. evidence 有效；
3. actual game time 足够；
4. claim 与验证单元匹配；
5. checkpoint 接受。

没有 checkpoint 的情况下，Codex 不得单方面写 “validated”。

## 14. Codex 的文档更新纪律

### 每轮必须更新 `docs/handoffs/latest.md`

必须写清：

1. 当前 task id
2. 本轮实际完成内容
3. 产生的 artifacts
4. 失败分类或 capability 结论
5. 下一允许任务

### 每轮必须更新 report

report 必须回答：

1. 这轮验证了什么；
2. 没验证什么；
3. 结果属于 `task completed`、`diagnostic completed` 还是 `capability validated`；
4. 若失败，dominant failure class 是什么；
5. 下一步是 rerun、repair、split 还是回退。

## 15. 最终执行纪律

Codex 在 research mode 下必须遵守下面这条总规则：

先保证顺序正确，再追求进度；
先保证证据有效，再追求结论；
先保证 baseline 成立，再追求 adaptive claim；
先保证 checkpoint 放行，再进入下一个 task。
