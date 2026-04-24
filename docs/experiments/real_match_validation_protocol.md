
# 真实对局验证协议

状态：active
更新日期：2026-04-23
适用范围：所有 gameplay capability 与 research contribution 相关任务
直接依赖：

* docs/foundation/04_research_direction/research_direction_decision.md
* docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md
* docs/plans/active/research_master_task_queue.yaml

## 一、协议目的

本协议不是为了规定一个僵硬的固定场次数，而是为了把“什么必须跑真实 SC2、什么不能跑、什么算有效证据、什么只能算诊断、什么情况下必须 rerun、repair 或 stop”写清楚。

本协议直接解决旧 Phase B 暴露出的四类问题：

1. 运行窗口不公平时，能力结论被误写。
2. diagnostic signal 被误写成 capability success。
3. batch / paired evaluation 的规模与 claim 不匹配。
4. checkpoint 没有一个统一、可复用的证据语言。

## 二、总则

1. 任何 gameplay capability claim，必须来自真实 SC2。
2. 任何 research contribution claim，必须来自真实 SC2 的 paired evaluation。
3. 任何 real-match run，必须带有 code provenance、config snapshot、match result、replay、telemetry summary。
4. 任何 claim 的验证规模，必须由它要验证的对象决定，而不是拍脑袋写一个固定场次。
5. 任何 evidence 若不能回答“它验证了什么、没验证什么、下一步是否允许继续”，就不是合格 evidence。

## 三、什么任务必须跑真实 SC2

以下任务必须跑真实 SC2，不能只靠单元测试、dry-run 或静态推理：

### 1. build chain 相关 claim

包括但不限于：

1. Gateway ready
2. Assimilator / Cybernetics Core 的真实机会窗口
3. opening build progression 是否真的成立
4. build stall 是否来自真实 gameplay，而不是 runner / config 问题

原因：
这些都是 gameplay capability，不是代码存在性。
它们只有在真实时间推进、真实资源流、真实地图与敌方存在的条件下才有意义。

它们验证什么：
真实 build progression 是否成立、是否被公平暴露、是否具备后续 production 前提。

它们不验证什么：
不验证 baseline strength，不验证 adaptive effect，不验证 broader generalization。

### 2. army production 相关 claim

包括但不限于：

1. combat-unit production
2. own_army_count>0
3. continued production
4. rally based on real army

原因：
如果不跑真实 SC2，就无法判断第一支 army 是否真的出现、是否只是命令发出、是否受 supply / gas / tech / runtime 限制影响。

它们验证什么：
友军 army 是否真实存在，以及 production 链条是否可进入战术阶段。

它们不验证什么：
不验证 defend / attack 是否稳定，不验证 Level 1 baseline 是否接受。

### 3. tactical / combat 相关 claim

包括但不限于：

1. defend_order
2. attack_order
3. friendly combat
4. regroup / fallback
5. target selection in contact

原因：
这些 claim 的本质是“army 在真实敌我接触中如何行为”，离开真实对局无法判断。

它们验证什么：
战术 order 是否建立在真实 army、真实敌情、真实接敌上。

它们不验证什么：
不自动等价于 batch-level baseline strength，也不自动等价于 research contribution。

### 4. baseline strength 或 Level claim

包括但不限于：

1. Level 1 playable baseline
2. repeated wins against designated easy slice
3. medium slice 可用性
4. broader opponent slice 稳定性

原因：
这些结论天然属于多局、真实对局层级，不能靠 probe、unit test 或单局印象得出。

它们验证什么：
某个 baseline 在指定 claim slice 上是否真的具备重复性与可玩性。

它们不验证什么：
不自动证明 adaptive effect，不自动外推到更广泛的对手池。

### 5. adaptive / opponent-model claim

包括但不限于：

1. continue_scouting 被 adaptive gate 改变
2. defensive_posture 被 adaptive gate 改变
3. first_attack_timing 被 adaptive gate 改变
4. adaptive layer 带来 outcome / robustness / failure-class 改善

原因：
research contribution 的核心是“这层 adaptive 逻辑是否真实改变了 gameplay，并且这种改变是否有收益”。
不跑真实 paired evaluation，就没有因果可归因性。

它们验证什么：
behavior delta、causal effect、研究特色是否成立。

它们不验证什么：
不自动证明 broader-pool generalization，除非另外跑 extension batch。

## 四、什么任务不能跑真实 SC2

以下任务不应消耗真实 SC2 预算；即使跑了，也不能用其结果做 gameplay 或 research claim：

### 1. 文档、分类、计划、协议任务

包括：

1. 研究方向重写
2. plan / queue / protocol 更新
3. asset reclassification
4. README / docs 重写

原因：
这些任务的正确性取决于事实一致性与逻辑一致性，不取决于对局结果。

### 2. 纯静态代码与配置任务

包括：

1. schema 改动
2. config role 重命名
3. runner provenance 字段补齐
4. artifact 路径或 manifest 结构调整

原因：
这类任务应该先通过静态检查、单元测试、dry-run 证明自己没有破坏执行合同。
过早消耗真实对局只会浪费预算。

典型例子：

1. 冻结 `debug_only` / `baseline_playable` / `adaptive_research` 三类 config role
2. 补齐 evaluation artifact 中的 `git_commit`、`config_snapshot`、`run_class`、`validation_class`
3. 让 dry-run 输出足以审计 provenance，但不把 dry-run 叙述成 gameplay evidence

### 3. 离线分析与报告整理任务

包括：

1. 读取已有 artifacts 生成报告
2. failure-class 排序
3. checkpoint 证据归档
4. replay 标注与索引整理

原因：
这些工作依赖已有 evidence，不应伪装成新 evidence。

### 4. 尚未满足前置能力的下游任务

包括：

1. build chain 未过时去跑 army / tactical batch
2. army 未过时去跑 friendly combat claim
3. Level 1 baseline 未过时去跑 adaptive paired evaluation

原因：
这类 real run 即使执行，也只会得到“missing prerequisite”的废证据，不能提升主线确定性。

## 五、什么任务在当前阶段禁止跑真实 SC2

“不能跑”与“当前阶段禁止跑”不同。

以下任务在技术上可以跑，但在当前主线阶段被禁止，因为它们会污染结论：

1. 在 baseline 未接受前，跑 broader opponent pool 展示 batch。
2. 在 adaptive feature 未冻结前，边改 baseline 边做 paired evaluation。
3. 在 dominant failure class 未修完前，同时跑多个修复方向的大 batch。
4. 用 debug config 做 capability claim。
5. 用 research prototype 直接混入 mainline real eval。

## 六、证据包要求

一组有效 real-match evidence，至少必须包含：

1. code provenance

   * 提交标识、工作区状态或等价可追溯信息
2. config snapshot

   * bot config
   * evaluation config
   * map / opponent slice
3. match result
4. replay
5. telemetry / event summary
6. phase-specific report
7. capability_validation_status 或 failure_class

若缺少其中任意关键项，本次 evidence 不能直接支持 capability claim。

### 当前 mainline config role 约定

当前主线固定使用以下三类 bot config 角色：

1. `debug_only`

   * 对应 `configs/bot/debug.yaml`
   * 只允许用于 smoke、dry-run、最短窗口调试
   * 禁止用于任何 gameplay capability claim

2. `baseline_playable`

   * 对应 `configs/bot/baseline_playable.yaml`
   * 是 Phase playable core rebuild 的正式 control config
   * 允许用于 build chain / production / tactical / small eval 等 baseline capability 验证

3. `adaptive_research`

   * 对应 `configs/bot/adaptive_research.yaml`
   * 是后续 adaptive research paired evaluation 的 treatment config
   * 只有在 baseline_playable 通过对应 checkpoint 后才允许进入 paired evaluation

`configs/bot/phase_b_revalidation_gameplay.yaml` 仅保留为过渡期 fallback / historical reference。
当 `baseline_playable.yaml` 已存在时，它不再是当前 mainline control config。

### 为什么需要这套证据包

它验证什么：

1. run 的确发生了；
2. run 属于哪个代码 / 配置版本；
3. claim 与 run 可以一一对应；
4. 后续 checkpoint 能审计 run，而不是靠口述。

它不验证什么：

1. 不自动验证阶段目标已完成；
2. 不自动证明稳定性；
3. 不自动证明研究因果性。

## 七、验证单元定义

### 1. probe

定义：
probe 是为一个单一 capability 或 blocker 设计的最小真实验证单元。

一个 probe 不等于“永远一局”。
当 claim 需要至少一次真实机会窗口、一次真实接敌、或一次真实行为触发时，probe 的规模是“拿到这次有效机会所需的最小运行集合”。

为什么需要这种规模：
因为 probe 的目标是回答“这个能力是否存在、是否被公平暴露、失败属于哪一类”，而不是回答稳定性。

probe 验证什么：

1. capability existence
2. fair opportunity
3. failure class
4. 是否有资格进入下一阶段

probe 不验证什么：

1. 稳定性
2. repeated wins
3. 研究因果效果
4. broader generalization

### 2. batch

定义：
batch 是围绕一个已存在的 capability，检查其在指定 claim slice 上是否具有重复性、覆盖性或稳定性的真实评测集合。

batch 的规模由三个维度共同决定：

1. 要覆盖的 opponent slice
2. 要覆盖的 map slice
3. probe 暴露出的结果方差

为什么需要这种规模：
因为稳定性与覆盖性不是单 probe 能回答的问题。
如果 claim 是“已经达到 Level 1 playable baseline”，就必须让 batch 去回答“这是不是可重复现象”。

batch 验证什么：

1. 某个 capability 是否稳定
2. 某个 baseline 是否在指定切片上具备重复性
3. dominant failure class 是什么

batch 不验证什么：

1. 单个设计改动的因果贡献
2. adaptive layer 的可归因效果
3. 对更广泛对手池的自动外推

### 3. paired evaluation

定义：
paired evaluation 是 control 与 treatment 的成对真实评测。
在本项目中，control 通常是 baseline_playable，treatment 通常是 adaptive_research。
两者除研究变量外，其余条件必须尽量一致。

paired evaluation 至少要在以下维度上匹配：

1. map slice
2. opponent slice
3. baseline core version
4. evaluation contract
5. artifact schema

为什么需要这种规模：
因为 research claim 不是“这个 bot 好像更强”，而是“这个 adaptive layer 引起了可归因的行为差异，并带来收益”。

paired evaluation 验证什么：

1. behavior delta
2. causal effect
3. 研究特色是否成立

paired evaluation 不验证什么：

1. 自动证明 broader-pool generalization
2. 自动证明所有 adaptive policy 都有效
3. 自动替代 baseline acceptance

## 八、什么是 capability validation

capability validation 同时满足以下条件，缺一不可：

1. claim 本身有明确对象

   * 例如 Gateway ready、own_army_count>0、friendly combat、Level 1 baseline、adaptive behavior delta
2. prerequisite 已满足

   * 例如未有 army 时不能验证 friendly combat
3. 机会窗口公平

   * 例如 build-chain claim 不可在短窗口中被强行下结论
4. 证据包完整
5. 采用了与 claim 相匹配的验证单元

   * probe、batch 或 paired evaluation
6. checkpoint 对该 claim 明确给出 accepted / not accepted 结论

capability validation 验证什么：
某个能力在真实、公平、可追溯条件下成立。

它不验证什么：

1. 它不自动升级为下一层能力；
2. 它不自动证明研究贡献；
3. 它不自动替代 broader-slice 结论。

## 九、什么是 diagnostic only

以下情形都属于 diagnostic only，而不是 capability validated：

1. 只看到 command telemetry，没有 ready / completion 证据。
2. own_army_count=0 时出现的 defend / attack / combat 相关信号。
3. 有 event、有 report、有 replay，但 prerequisite 未满足。
4. run 因 runtime / config 问题提前截断，只能证明 blocker，不足以证明能力。
5. opponent-model 只改变了 response tag，没有改变 gameplay gate。
6. batch 或 paired evaluation 的 artifact 完整，但 claim 与验证单元不匹配。

diagnostic only 验证什么：
哪里有信号、哪里有 blocker、下一步应该修哪一类问题。

它不验证什么：
目标能力本身是否成立。

## 十、什么是 insufficient_duration

insufficient_duration 的定义不是“时间短”这么简单，而是：

在当前 claim 所需的最小公平机会窗口尚未满足之前，run 已经结束，而且这个结束本身并不能自然地回答该 claim。

例子：

1. 想验证 Gateway ready，但窗口还没走到，run 就因为错误配置提前结束。
2. 想验证 friendly combat，但 army 尚未形成、接敌窗口尚未出现，run 就被截断。
3. 想验证 paired adaptive effect，但其中一边 run 持续时间不足以让相关门控实际触发。

insufficient_duration 验证什么：
当前证据不能公平回答该 claim，先别下 gameplay 结论。

它不验证什么：

1. 不证明能力失败；
2. 不证明能力成功；
3. 不等价于 logic failure。

## 十一、什么是 invalid evidence

以下任一情形出现，该 evidence 直接判为 invalid：

1. 缺 replay
2. 缺 match result
3. 缺 config snapshot
4. code / config provenance 不可追溯
5. 同一 batch 中混入了不同逻辑版本但未声明
6. 用 debug config 跑 capability claim
7. human manual intervention 改变了 run 行为
8. runner / telemetry / replay 记录互相冲突
9. paired evaluation 中 control 与 treatment 不可比
10. 已知 prerequisite 未满足却继续把 run 当目标证据
11. report 结论与 raw evidence 不一致

invalid evidence 验证什么：
只验证了一件事：这组证据不能用。

它不验证什么：
任何 gameplay 或 research 结论。

## 十二、什么是 rerun

rerun 指的是：

在不改变 claim、或只做最小合法修正的情况下，重新执行与原任务同级的验证单元，以修复 invalid evidence 或确认边界性结果。

### rerun 适用场景

1. invalid evidence
2. paired run 中一侧缺失
3. batch 中某个切片 artifact 损坏
4. borderline 结果需要最小确认

### rerun 不适用场景

1. 已明确 logic failure，却不愿修代码
2. prerequisite 未满足，却希望靠多跑几局蒙混过去
3. 想扩大样本来掩盖错误分类

## 十三、什么是 repair

repair 指的是：

针对已明确的 dominant failure class，做一次范围受控的代码、配置或验证设计修正，然后回到与该 failure class 对应的最小必要验证单元。

### repair 必须满足

1. repair 目标唯一明确
2. repair 范围受控
3. repair 之后必须 rerun
4. repair 不得偷偷引入第二个研究变量

### repair 验证什么

它验证什么：
当前 failure class 是否被有效处理。

它不验证什么：

1. 不自动验证整个 phase 成功；
2. 不自动允许跳过 checkpoint；
3. 不自动允许进入更高 phase。

## 十四、什么是 stop

stop 是正式停止前进，不是“先记一下”。

以下情形必须 stop：

1. checkpoint minimum gate 未通过
2. evidence invalid 且尚未 rerun
3. prerequisite regression 被发现
4. 当前 phase 的 dominant failure class 未被 repair
5. baseline 未接受却有人试图进入 adaptive phase
6. adaptive paired evaluation 期间 baseline core 仍在漂移

stop 之后允许的动作只有三类：

1. rerun
2. repair
3. return_to_prior_phase

不允许“先往后跑一点看看”。

## 十五、验证规模如何选择

本协议不提供一个全局固定场次数字。
验证规模必须由 claim 类型决定。

### 1. 当 claim 是“能力是否存在”

使用 probe。

为什么需要这个规模：
要回答 existence，只需要最小有效机会窗口，不需要先追求广泛重复。

它验证什么：
能力有没有、窗口公不公平、failure class 是什么。

它不验证什么：
稳定性与强度。

### 2. 当 claim 是“能力是否稳定”

使用 batch。

为什么需要这个规模：
稳定性只能在代表性切片上被观察，probe 无法覆盖方差。

它验证什么：
重复性、覆盖性、dominant failure class。

它不验证什么：
单一设计改动的因果贡献。

### 3. 当 claim 是“adaptive layer 是否带来因果效果”

使用 paired evaluation。

为什么需要这个规模：
研究结论必须有 control / treatment 可比性，不能只看单边强不强。

它验证什么：
behavior delta、causal effect、研究特色是否成立。

它不验证什么：
broader-pool 泛化。

### 4. 当 claim 是“可否对外展示或扩展到更广切片”

使用 extension batch。

为什么需要这个规模：
展示与扩展关心边界与覆盖，而不是只关心核心因果命题本身。

它验证什么：
已接受结论在更广切片上的边界。

它不验证什么：
不会反向替代 core claim 的成立。

## 十六、失败类别到动作的映射

### invalid_evidence

动作：
rerun same claim，保持代码不变。

### insufficient_duration

动作：
先修 runtime / evaluation contract，再回到原 claim。

### missing_prerequisite

动作：
回退到前一阶段 capability，不得继续下游验证。

### logic_failure

动作：
做受控 repair，然后 rerun 对应 probe 或 batch。

### stability_failure

动作：
在当前阶段做 focused repair 或 confirmation，不得偷换成 broader claim。

### no_behavior_change

动作：
只针对 adaptive gate repair，不得扩大 paired eval 规模掩盖问题。

### no_causal_benefit

动作：
冻结结论为“adaptive effect 未接受”，然后决定是否继续单变量 repair。

### regression

动作：
立刻回到上一个通过 checkpoint 的 control 版本，禁止在漂移状态下继续评测。

## 十七、当前仓库的直接适用约束

1. 旧 Phase B 产出的短窗口 run，一律不能作为 build-chain、army、combat、Level 1 baseline 的 capability validation。
2. Phase B-R duration probe 只证明“窗口公平性前提已恢复一次”，不自动证明任何 gameplay capability。
3. rule-based opponent model 当前只到 telemetry / response-tag 基线，不得在 paired evaluation 之前写成 adaptive success。
4. debug config 只允许用于 debug，不得再出现在正式 capability report 或 research report 中。

## 十八、checkpoint 输出要求

每次 checkpoint 必须显式写：

1. reviewed_tasks
2. minimum_gate_passed
3. target_gate_passed
4. stretch_gate_status
5. evidence_paths
6. capability_validation_status
7. failure_class
8. decision
9. next_allowed_task

其中：

* minimum_gate_passed 决定能否继续前进；
* target_gate_passed 决定本阶段是否真正达到设计目标；
* stretch_gate_status 决定是否为扩展阶段提供低风险起点；
* next_allowed_task 必须是具体 repair、rerun、prior-phase return 或 accepted_continue。

## 十九、协议的最终作用

本协议不是让项目变保守，而是防止项目继续把“跑过了”“记下了”“看起来有信号”误写成“能力成立”。

从本协议生效起，任何真实对局验证都必须明确回答：

1. 它验证了什么；
2. 它没有验证什么；
3. 它属于 probe、batch 还是 paired evaluation；
4. 它是 capability validated、diagnostic only、insufficient_duration 还是 invalid evidence；
5. 它之后允许继续、必须 repair、还是必须 stop。
