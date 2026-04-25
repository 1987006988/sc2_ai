# Phase R6 Temporal Opponent Belief Frontier

状态：active
更新日期：2026-04-25
角色：R6 执行手册
适用范围：从 `project_core_goal_reached` 之后启动的前沿扩展

直接依赖：

- `docs/foundation/04_research_direction/r6_temporal_opponent_belief_frontier_decision.md`
- `docs/plans/active/R6_FRONTIER_MASTER_EXECUTION_PLAN.md`
- `docs/plans/active/r6_frontier_task_queue.yaml`
- `docs/experiments/r6_frontier_evaluation_protocol.md`
- `docs/experiments/r6_claims_and_interview_deliverables.md`

## 1. R6 的唯一问题

R6 不再回答“这个 bot 能不能打起来”。  
R6 唯一回答：

> 一个 replay-trained temporal opponent belief，是否能在 partial observability 下恢复隐藏敌方状态，并通过 bounded macro response 在 internal + external evaluation 中带来稳定收益。

## 2. R6 的代码边界

### 2.1 belief model 相关边界

优先修改或新增文件：

- `src/sc2bot/domain/belief_state.py`
- `src/sc2bot/opponent_model/interface.py`
- `src/sc2bot/opponent_model/rule_based_model.py`
- `src/sc2bot/opponent_model/temporal_belief_model.py`
- `src/sc2bot/opponent_model/temporal_belief_adapter.py`
- `src/sc2bot/opponent_model/feature_encoder.py`
- `src/sc2bot/opponent_model/inference_runtime.py`

原则：

1. `belief_state.py` 继续作为统一 belief object，不允许被 dict 污染。
2. learned model 不直接碰 gameplay。
3. `rule_based_model.py` 保留为 comparator，不删除、不隐式覆盖。

### 2.2 决策接入边界

优先修改文件：

- `src/sc2bot/managers/strategy_manager.py`
- `src/sc2bot/runtime/game_loop.py`
- `src/sc2bot/managers/tactical_manager.py`
- `configs/bot/baseline_playable.yaml`
- `configs/bot/adaptive_research.yaml`
- `configs/bot/r6_learned_belief.yaml`

原则：

1. `strategy_manager.py` 是 belief -> bounded response surface 的唯一入口。
2. `tactical_manager.py` 只承接被允许的 response surface，不接 learned policy。
3. `r6_learned_belief.yaml` 仅包含 learned belief treatment 所需差异，不改 frozen baseline。

### 2.3 数据与训练边界

建议新增目录：

- `research/r6_temporal_belief/data/`
- `research/r6_temporal_belief/datasets/`
- `research/r6_temporal_belief/labels/`
- `research/r6_temporal_belief/models/`
- `research/r6_temporal_belief/train/`
- `research/r6_temporal_belief/eval/`
- `research/r6_temporal_belief/cards/`
- `scripts/r6/`

### 2.4 配置边界

建议新增：

- `configs/research/r6_dataset_manifest.yaml`
- `configs/research/r6_label_schema.yaml`
- `configs/research/r6_train_gru.yaml`
- `configs/research/r6_train_transformer.yaml`
- `configs/research/r6_train_ssm.yaml`
- `configs/evaluation/r6_internal_paired_easy.yaml`
- `configs/evaluation/r6_internal_paired_medium.yaml`
- `configs/evaluation/r6_external_house_bots.yaml`

原则：

1. 不在 `baseline_playable.yaml` 里堆训练参数。
2. 不在 `adaptive_research.yaml` 里混入 learned model 超参数。
3. 训练 config、在线 treatment config、evaluation config 必须分离。

### 2.5 报告与证据边界

建议新增：

- `artifacts/reports/r6_control_anchor/report.md`
- `artifacts/reports/r6_offline_benchmark/report.md`
- `artifacts/reports/r6_learned_belief_training/report.md`
- `artifacts/reports/r6_internal_paired/report.md`
- `artifacts/reports/r6_external_eval/report.md`
- `artifacts/reports/checkpoints/r6_checkpoint_*.md`

原则：

1. R6 报告必须区分 offline / online / external 三类证据。
2. 不允许用 offline accuracy 替代 online gain。
3. 不允许用 online gain 替代 external evidence。
4. 不允许用最终 narrative 替代 per-run artifact。

## 3. R6 的分层子阶段

### P0：control freeze 与 claim contract

目标：冻结 accepted baseline 与 accepted R5 adaptive comparator，避免后续训练和评测改写历史控制组。

### P1：replay benchmark 与 label pipeline

目标：建立 hidden-state benchmark，而不是直接冲 online win rate。

### P2：learned temporal belief

目标：训练 learned model，先在离线任务上超过非学习基线。

### P3：decision-aware online integration

目标：让 learned belief 进入在线决策，并在 internal paired evaluation 中证明它比 frozen baseline 和 frozen R5 comparator 更有价值。

### P4：external validation 与 interview closeout

目标：把结果从内部 paired evaluation 推到外部 bot 生态，并生成面试级证据包。

## 4. R6 的证据规则

### 什么只算实现完成

1. 代码写完
2. 测试过
3. 模型能训练或能推理
4. 配置能加载

### 什么只算 offline diagnostic

1. 某个 label 能提取但不稳定
2. 模型只在单一任务上偶然超过 baseline
3. calibration 明显坏掉
4. split 泄漏风险未完全排除

### 什么才算 offline capability validated

1. leakage-safe benchmark 成立
2. learned model 与 baselines 可比
3. holdout report 完整
4. checkpoint 接受

### 什么只算 online diagnostic

1. tag 变了但行为没变
2. behavior 变了但 paired 不可比
3. outcome 变了但 control drift
4. 只在单一 anecdotal run 出现优势

### 什么才算 online capability validated

1. 三臂 paired eval 可比
2. 行为差异明确
3. 收益方向一致
4. checkpoint 接受

### 什么才算 frontier accepted

1. offline target 通过
2. online target 通过
3. external target 通过
4. interview evidence pack 完整
5. frontier checkpoint 接受
