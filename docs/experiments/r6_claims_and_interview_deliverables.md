# R6 Claims and Interview Deliverables

状态：active
更新日期：2026-04-25
作用：定义 R6 结束时必须拿出来讲的研究 claim 和证据包

直接依赖：

- `docs/foundation/04_research_direction/r6_temporal_opponent_belief_frontier_decision.md`
- `docs/plans/active/R6_FRONTIER_MASTER_EXECUTION_PLAN.md`
- `docs/experiments/r6_frontier_evaluation_protocol.md`

## 1. 面试时允许讲的核心命题

只有当 R6 完成后，才允许讲下面这个命题：

> 我们提出并验证了一个 replay-trained temporal opponent belief system，用来恢复 StarCraft II partial observability 下的隐藏敌方状态；该 belief 不只是提高离线预测指标，而且通过 bounded macro response 改变在线行为，并在 internal paired evaluation 与 external bot environment 中带来可归因收益。

## 2. 面试时绝对不要讲的东西

1. 我们已经接近 AlphaStar
2. 我们已经达到 ladder 顶尖水平
3. 我们的方法对所有对手都有效
4. 我们做了一个通用世界模型
5. 我们做成了第二个 adaptive feature
6. 我们已经证明全部泛化

## 3. R6 完成后必须能展示的四层证据

### A. 当前起点

1. R0-R5 完成了什么
2. 当前 frozen baseline 是什么
3. 当前 accepted R5 comparator 是什么
4. 为什么这还不够构成前沿研究

### B. Offline 研究证据

1. benchmark task 列表
2. rule-based / static / shallow temporal / learned temporal 对照表
3. calibration 图或误差图
4. 至少一组 ablation

### C. Online 决策证据

1. A/B/C 三臂配置表
2. 行为差异统计表
3. outcome / robustness / failure-class 对照表
4. 2 到 3 个代表性 replay case

### D. External 生态证据

1. external environment 简介
2. external slice 结果表
3. 外部 replays 或 replay index
4. internal 与 external 结果的边界解释

## 4. 结果总表模板

最终必须产出一张总表，至少包含：

1. Setting
2. Slice
3. Comparator
4. Treatment
5. Win rate
6. Key behavior delta
7. Primary evidence path
8. Claim status
9. Notes / caveats

## 5. 图表最少集合

至少需要以下图表：

1. offline benchmark leaderboard
2. calibration or uncertainty plot
3. internal paired win-rate bar / table
4. gate activation distribution comparison
5. external eval result table
6. one-page claim boundary chart

## 6. replay / demo 最少集合

至少准备：

1. 一个 baseline failure case
2. 一个 learned belief 成功识别隐藏敌情的 case
3. 一个 learned response 改变 scout budget 的 case
4. 一个 learned response 改变 attack timing 或 production tempo 的 case
5. 一个 external bot environment case

## 7. 面试叙事结构

建议固定 7 步：

1. 先说明为什么当前 accepted project 还不够前沿
2. 再说明 partial observability 才是下一步主问题
3. 说明为什么规则 opponent model 不够
4. 说明 learned temporal belief 的核心设计
5. 说明为什么要用 bounded response surface，而不是全局策略重写
6. 说明 offline -> online -> external 三层验证链
7. 最后明确边界，不夸大

## 8. 面试时最重要的对比对象

至少要能清晰比较三条线：

1. frozen accepted baseline
2. frozen accepted R5 rule-based adaptive
3. R6 learned temporal belief treatment

## 9. 交付物清单

R6 closeout 时必须存在：

1. `artifacts/reports/r6_frontier_closeout/report.md`
2. `artifacts/reports/r6_internal_paired/report.md`
3. `artifacts/reports/r6_external_eval/report.md`
4. `artifacts/reports/r6_offline_benchmark/report.md`
5. `research/r6_temporal_belief/cards/model_card.md`
6. `research/r6_temporal_belief/cards/dataset_card.md`
7. one-page results table
8. replay/demo index
9. claim boundary page

## 10. 通过标准

只有当以下都成立时，才算 interview-ready：

1. 每个主张都能指到具体 artifact
2. 无效证据已被明确剔除
3. 优势不是只来自 built-in Easy 单切片
4. 外部 bot 生态至少有一个正向 slice
5. 能用一句话说明提升点、提升范围、边界条件
