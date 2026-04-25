# R6 Frontier Master Execution Plan

状态：active
更新日期：2026-04-25
作用：R6 前沿扩展主计划
激活方式：仅在明确进入 R6 frontier mode 时激活
与旧主线关系：R0-R5 主计划保留为已完成核心计划；R6 是新增扩展计划，不回写已接受的旧结论

直接依赖：

- `docs/foundation/04_research_direction/r6_temporal_opponent_belief_frontier_decision.md`
- `docs/plans/active/r6_frontier_task_queue.yaml`
- `docs/experiments/r6_frontier_evaluation_protocol.md`
- `docs/experiments/r6_claims_and_interview_deliverables.md`

## 一、R6 总目标

把当前项目从“已接受的 Level 1 baseline + 一个窄切片 rule-based adaptive 结果”，推进到“具有更强研究说服力的 learned temporal opponent belief system”。

R6 的总目标不是泛泛提高 win rate，而是同时完成：

1. 离线 hidden-state benchmark
2. 学习型时序 belief
3. decision-aware online integration
4. 外部生态验证
5. 面试级证据包

## 二、R6 不做什么

R6 明确不做：

1. 推翻已接受 baseline
2. 同时追多个研究特色
3. 直接追 full self-play league training
4. 大规模 end-to-end policy learning
5. 重新回到“先把 bot 变得更能跑”的工程主线
6. 用对外包装替代新证据
7. 在没有 external validation 的前提下自称前沿

## 三、R6 的阶段划分

### Phase R6.0：Control Freeze 与 Data Contract

冻结当前 accepted baseline 与 R5 accepted adaptive 为历史控制组；建立 replay 数据、split、label、manifest 的统一契约，避免训练和评测发生数据泄漏或 control drift。

### Phase R6.1：Offline Hidden-State Benchmark

先把研究问题量化清楚，建立 hidden-state recovery benchmark，并为 learned model 设定 rule-based 与 static baselines。

### Phase R6.2：Learned Temporal Belief Model

训练 learned temporal model，并在 offline benchmark 上超过 rule-based / static baselines。

### Phase R6.3：Decision-Aware Online Integration

将 learned belief 接到 bounded response surface，并通过三臂内部 paired evaluation 验证它不只是更会预测，而是真实改变行为并带来收益。

三臂定义：

1. A：frozen accepted baseline_playable
2. B：frozen accepted R5 rule-based adaptive
3. C：R6 learned temporal belief treatment

### Phase R6.4：External Bot Validation 与 Interview Closeout

把结论从内部 paired evaluation 推到外部 bot 生态，并形成顶级面试可用的证据包。

## 四、阶段推进硬规则

1. R6.0 不通过，后续阶段 blocked。
2. R6.1 不通过，不能训练 learned model 并宣称前沿。
3. R6.2 不通过，不能进入 online integration。
4. R6.3 不通过，不能进入 external frontier claim。
5. R6.4 不通过，不能对外讲“frontier-level result”。

## 五、R6 的真实证据分层

### 基础证据层

1. code provenance
2. config snapshot
3. dataset version
4. split manifest
5. training seed / eval seed
6. report / checkpoint

### 离线研究证据层

1. benchmark summary
2. per-task metrics
3. calibration / uncertainty diagnostics
4. baseline vs learned comparison
5. ablation results

### 在线研究证据层

1. matched internal paired artifacts
2. 三臂 control/comparator/treatment 的一致性证明
3. behavior delta summary
4. outcome / failure-class delta
5. replay-backed case study

### 外部生态证据层

1. external bot environment config
2. bot package manifest
3. results summary
4. replays
5. comparative table

## 六、R6 的主要 failure classes

1. dataset_leakage_or_split_failure
2. label_contract_failure
3. weak_temporal_model
4. calibration_regression
5. online_behavior_change_absent
6. online_causal_benefit_absent
7. control_drift
8. external_eval_mismatch
9. interview_evidence_incomplete

## 七、R6 repair 原则

1. 一次只修一个 dominant failure class
2. 离线失败先在离线修，不得拿 online batch 掩盖
3. online failure 先检查三臂可比性，再判断模型弱
4. external failure 先检查环境一致性，再判断泛化失败
5. interview evidence 不足时，不得反向夸大研究结论

## 八、R6 完成定义

R6 只有在以下条件同时成立时，才算完成：

1. R6.2 的 learned temporal belief 在 offline benchmark 上通过 target gate
2. R6.3 的 learned treatment 在 internal paired evaluation 上通过 target gate
3. R6.4 的 external validation 与 interview package 通过 target gate
4. frontier checkpoint 正式接受

## 九、R6 输出给面试的最终一句话

> 我们做出的不是另一个规则 bot，而是一个用公开 replay 数据学习时序对手信念、并把该信念转化为 bounded macro decisions 的 SC2 full-game system；它在离线隐藏状态恢复、内部 matched paired evaluation 和外部 bot 生态中都获得了可归因收益。
