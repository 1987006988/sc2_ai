# R6 Temporal Opponent Belief Frontier Decision

状态：active
更新日期：2026-04-25
角色：R6 前沿扩展方向决策文件
生效方式：仅在明确进入 R6 frontier mode 时生效
前置状态：R0-R5 核心主线已接受完成；旧主队列保留为已完成记录，不再驱动新研究主线

## 一句话总定位

R6 的唯一主研究方向是：学习一个基于 replay 的时序对手信念模型，用它恢复 Fog of War 下的隐藏敌方状态，并以 decision-aware 的方式驱动在线宏观响应，在多地图、多对手种族、内部 paired evaluation 与外部 bot 生态中验证可归因收益。

## 启动前提

R6 不推翻 R0-R5。R6 建立在以下已接受前提之上：

1. 一个 Level 1 playable Protoss baseline 已被接受。
2. 一个 rule-based sparse-scout adaptive gating feature 已被接受。
3. 当前仓库已经具备 real-match、batch、paired evaluation、checkpoint、failure-class、repair 执行纪律。
4. 旧主队列已经收口到 `project_core_goal_reached`，因此 R6 必须以扩展计划方式启动。

## 主研究问题

在一个已经通过真实对局验收的 Protoss baseline 上，是否可以通过时序 replay 学习得到一个比当前 rule-based placeholder 更强的 opponent belief model，使其在以下两层同时取得可验证收益：

1. 离线层：对隐藏 tech、隐藏 army、未来接敌、扩张风险、time-to-contact 等关键隐藏状态的恢复能力，稳定优于 rule-based 与 static baselines。
2. 在线层：通过一个有边界的 response surface，真实改变 scout budget、defensive posture、first-attack timing 与 production tempo，并在多地图、多种族、内外部 bot 环境中产生方向一致的 outcome 改善。

## R6 只允许保留的主研究特色

R6 只保留一个研究特色：

`learned temporal opponent belief conditioned response surface`

它由两个不可分割的部分组成：

1. learned temporal belief
2. belief-conditioned bounded response surface

如果只做前者而不进入在线决策，它只是预测模型项目。  
如果只做后者而不学习 belief，它只是规则工程扩写。  
R6 只接受两者同时成立的系统。

## R6 允许影响的决策边界

R6 response surface 只允许作用于以下四类 gate：

1. continue_scouting / scout budget
2. defensive_posture
3. first_attack_timing
4. bounded production tempo
   - 允许影响 `gateway_target_count`、army buffer、attack readiness threshold
   - 不允许变成完全开放的 build-order generator

## R6 明确禁止的方向

以下方向都不是 R6 主线：

1. 直接追求 ladder competitiveness 叙事
2. 新开第二个 adaptive feature
3. multi-race 主体扩展
4. 端到端 full-game self-play league training
5. 全局 macro policy 重写
6. micro RL 或 combat-only branch
7. LLM 指挥器替代现有 decision stack
8. 只做更漂亮的 telemetry / report
9. 只做 dataset / benchmark 而不做 online decision integration
10. 只做内网 demo，不做外部 bot 生态验证

## 为什么 R6 不是继续堆当前 rule-based adaptive

当前 adaptive 已接受结果是一个窄切片、窄 feature、窄 gate 的真实结果。它证明了方向可行，但还没有形成足够强的前沿研究命题。继续在 rule-based placeholder 上加规则，只会继续提升工程完成度，不会形成足够强的研究叙事。R6 必须从“规则对手状态估计”升级到“可训练的时序 hidden-state recovery + decision-aware online adaptation”。

## 为什么 R6 不是直接冲 AlphaStar 路线

R6 明确不走“复现 AlphaStar”路线。原因不是目标降低，而是策略重排：

1. 当前仓库已有一个可玩的 full-game baseline 与可审计 evaluation discipline。
2. 当前最短的前沿跃迁路径，不是大规模 self-play，而是利用公开 replay 数据与 offline benchmark，把 partial observability 下的 belief learning 做扎实。
3. 如果没有先把 learned belief 在离线与中等规模在线 setting 中做强，直接上大规模 self-play 只会把研究命题稀释成基础设施与算力竞争。

## R6 成功定义

R6 只有在以下四层同时成立时才算完成：

1. 数据与 benchmark 成立
   - 有泄漏受控的数据契约
   - 有隐藏状态任务定义
   - 有可复现实验 splits 与 baseline floor
2. learned belief 成立
   - 在 holdout offline benchmark 上，learned temporal model 稳定优于 rule-based / static baselines
3. decision-aware online claim 成立
   - 相对 frozen Level 1 baseline 与 frozen R5 rule-based adaptive，两者至少其一被 learned treatment 稳定超过，且行为差异与收益方向一致
4. 外部生态 claim 成立
   - 在 AI Arena 本地 house-bot 或等价 external bot slice 上，出现正向结果

## R6 失败定义

出现以下任一情况，R6 必须停止当前 claim、回到 repair：

1. 离线 benchmark leakage 不可控
2. learned model 不优于 static / rule-based baselines
3. online win-rate 提升无法归因到 learned belief
4. control、R5 rule-based adaptive、R6 learned treatment 三者不可比
5. AI Arena / external eval 完全无法复现内部结论
6. response surface scope creep，变成新的全局策略系统
7. 证明链依赖手工挑 run 或污染对照

## R6 完成后可对外主张的东西

只有 R6 全部通过后，才允许对外主张：

1. 我们不只是做了一个可玩 baseline，而是做了一个 replay-trained temporal opponent belief system。
2. 这个系统在 Fog of War 下恢复隐藏敌方状态，且这种恢复能通过 online macro decisions 转化为真实收益。
3. 这个收益不是只存在于 built-in Easy 单切片，而是通过多切片内部 paired eval 与外部 bot 环境得到支撑。

## R6 绝不允许对外主张的东西

即使 R6 完成，也不允许自动主张：

1. 我们已达到 AlphaStar / 顶级 ladder bot 水平
2. 我们已证明 broader-pool 普遍泛化
3. 我们的 learned belief 已是最优对手模型
4. 我们已完成第二个 adaptive feature
5. 我们已完成端到端 full-game learning

## R6 的面试价值目标

R6 的理想面试叙事应当是：

> 我不仅建立了真实对局验收链条，还提出并验证了一个针对 SC2 partial observability 的时序对手信念建模方法，并证明它能通过 bounded macro decisions 在多切片和外部 bot 生态中产生稳定收益。
