# R6 Frontier Evaluation Protocol

状态：active
更新日期：2026-04-25
作用：R6 研究验收协议
适用范围：offline benchmark、internal paired evaluation、external bot ecosystem evaluation

直接依赖：

- `docs/foundation/04_research_direction/r6_temporal_opponent_belief_frontier_decision.md`
- `docs/plans/active/R6_FRONTIER_MASTER_EXECUTION_PLAN.md`
- `docs/plans/active/r6_frontier_task_queue.yaml`

## 1. 总原则

R6 必须同时建立三类证据：

1. offline hidden-state recovery evidence
2. online decision-aware paired evidence
3. external bot ecosystem evidence

任何单一层级都不能替代其他层级。

## 2. Offline Benchmark 的对象

R6 offline benchmark 至少覆盖以下任务中的三项，target 应覆盖全部：

1. opening class
2. hidden tech path
3. future expansion within horizon
4. hidden army bucket
5. future contact risk
6. time-to-first-contact
7. next macro threat indicator

## 3. Offline 数据规则

### 数据源类别

允许使用四类来源：

1. public replay corpora
2. public benchmark datasets
3. local accepted replay artifacts
4. local historical replay corpora

### 数据源边界

1. public corpora 用于主训练与主 benchmark
2. local accepted replays 只允许作为补充 domain anchor，不允许污染 holdout benchmark
3. local historical replay corpora 可以用于 benchmark repair 或 benchmark bootstrapping，但必须：

   * 明确区分于 accepted R4/R5 anchors
   * 在 manifest 中记录 provenance、split role、usage boundary
   * 不得和 accepted artifact tables 混合讲述
4. internal online eval replays 不允许回流到同一轮 holdout benchmark

### split 规则

1. split 必须以 replay source manifest 为基础
2. 必须防止 replay pack、series、player、time-window 泄漏
3. 同一连串比赛中的相邻 replay 不得跨 train/test 混放
4. 任何人工挑选样本都必须在 manifest 中显式记录

## 4. Offline Metrics

每个任务至少定义一个主指标和一个稳定性指标。

建议主指标：

1. class tasks：macro-F1 / balanced accuracy
2. binary risk tasks：AUROC / AUPRC
3. horizon event tasks：top-k hit rate 或 recall at horizon
4. time tasks：MAE / interval accuracy

建议稳定性指标：

1. calibration ECE
2. Brier score
3. per-slice variance
4. confidence-conditional error

## 5. Offline Comparator Set

R6 offline comparator 至少包括：

1. current rule-based placeholder
2. static prior baseline
3. shallow temporal baseline
4. learned temporal model

## 6. Offline Claim 等级

### Offline minimum

1. benchmark leakage-safe
2. learned temporal model 至少在一个核心任务上超过 rule-based / static baseline
3. 结果可复现

### Offline target

1. learned model 在核心任务束上整体超过 comparator set
2. calibration 未显著恶化
3. ablation 能说明收益来自 temporal belief，而不是 incidental leakage

### Offline stretch

1. 多种 architecture / history window 结果方向一致
2. 迁移到新切片仍有正向结果

## 7. Online Internal Evaluation 的对象

R6 在线评测是三臂：

1. Arm A：frozen accepted baseline_playable
2. Arm B：frozen accepted R5 rule-based adaptive
3. Arm C：R6 learned temporal belief treatment

## 8. Online Internal 配对规则

每一个 triple-set 必须对齐：

1. map
2. opponent
3. race slice
4. evaluation contract
5. core baseline version
6. artifact schema

## 9. Online Behavior Delta 的定义

以下才算 R6 online behavior delta：

1. scout budget / scout persistence 出现可重复差异
2. defensive posture 时机出现可重复差异
3. first attack timing 出现可重复差异
4. bounded production tempo 出现可重复差异

以下不算：

1. tag 变了但行为没变
2. telemetry 更丰富了
3. 单次随机 timing 摆动
4. 战术 order 数量变化但没有执行后果

## 10. Online Outcome Delta 的定义

以下才算有效 outcome delta：

1. learned treatment 相对 Arm A 或 Arm B 出现方向一致的 win-rate / robustness / failure-class 改善
2. 这种改善可回指到行为差异
3. control/comparator/treatment 的 baseline core 没漂移

## 11. Online Internal Claim 等级

### Online minimum

1. 三臂可比
2. learned treatment 有行为差异
3. 无 baseline-core drift

### Online target

1. easy + medium 都有 valid paired evidence
2. learned treatment 相对 Arm A 和 Arm B 至少其一有方向一致收益
3. 报告能解释收益主要来自哪个 gate

### Online stretch

1. 多地图多种族都正向
2. offline gains 与 online gains 可对应

## 12. External Bot Evaluation 的对象

R6 external eval 优先采用：

1. AI Arena local-play-bootstrap
2. downloadable house bots
3. 与 AI Arena 兼容的 map/bot environment

## 13. External Eval 规则

1. external eval 不得使用与 internal eval 完全不同的 bot core
2. 若 external 环境需要轻微包装，包装只能影响运行兼容性，不得改变策略逻辑
3. external eval 报告必须把 internal 和 external 结果分开写

## 14. External Claim 等级

### External minimum

1. 至少一个 valid external slice
2. replays、results、manifest 完整
3. learned treatment 与 internal claim 的方向不冲突

### External target

1. 至少一个 external slice 为正向
2. 结论不建立在单个 polluted or cherry-picked run 上
3. enough evidence exists to say the method is not only a built-in-AI artifact

### External stretch

1. 多个 external bots 或多个 external slices 正向
2. 结果可作为公开展示材料

## 15. Invalid Evidence 规则

以下任一出现则 evidence invalid：

1. dataset split 泄漏
2. checkpointed control drift
3. polluted control 未排除
4. inconsistent model checkpoint / config / report mapping
5. external env mismatch
6. mixed valid and invalid runs in the same accepted table
7. replay/result/summary missing for load-bearing runs

## 16. Rerun 规则

以下情况必须 rerun，不得立即改 claim：

1. benchmark run interrupted
2. summary or metric file incomplete
3. paired triple-set 某一臂缺失
4. external env launch failure
5. accepted table accidentally mixed polluted and clean evidence

## 17. Repair 规则

以下情况必须 repair：

1. label contract failure
2. learned model long-run underfitting
3. behavior delta absent
4. comparator drift
5. external env incompatibility
6. interview evidence package mapping incomplete

repair 之后必须回到同级验证单元：

1. offline failure -> offline rerun
2. online failure -> internal paired rerun
3. external failure -> external rerun

## 18. R6 Frontier Claim 接受条件

R6 只有在以下条件全部满足时，才允许被 `checkpoint_K` 接受：

1. offline target passed
2. online target passed
3. external target passed
4. every top-line claim has exact evidence paths
5. invalid evidence is explicitly excluded
6. the claim remains within the single-feature boundary
