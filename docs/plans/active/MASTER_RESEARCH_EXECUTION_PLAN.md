
# MASTER_RESEARCH_EXECUTION_PLAN

状态：active
更新日期：2026-04-23
作用：这是当前仓库的唯一主执行计划文件。旧的 active 计划与阶段计划继续保留为历史背景，但不再单独决定任务优先级。
直接依赖：

* docs/foundation/04_research_direction/research_direction_decision.md
* docs/foundation/04_research_direction/retain_rewrite_drop_matrix.md
* docs/experiments/real_match_validation_protocol.md
* docs/plans/active/research_master_task_queue.yaml

## 一、总目标

建立一个单一种族 Protoss 的全游戏 SC2 智能体，并完成以下两个层级的真实验收：

1. 先完成 gameplay 层级的真实 playable core：

   * opening build chain 被真实验证；
   * combat-unit production 与 friendly army 被真实验证；
   * defend / attack / friendly combat 被真实验证；
   * non-adaptive baseline 在真实 batch 中达到 Level 1 playable baseline 接受标准。

2. 再完成 research 层级的真实 adaptive claim：

   * 只保留一个研究特色：稀疏侦察驱动的在线对手状态推断与时机门控层；
   * 该 adaptive layer 在 matched real-match paired evaluation 中，真实改变行为；
   * 该行为差异与 outcome / robustness / failure-class 改善方向一致，形成可归因研究贡献。

只完成第 1 层，不算完成项目研究目标。
只完成 telemetry、report、diagnostic，也不算完成 gameplay 目标。

## 二、仓库审计后的真实起点

当前仓库起点不是“从零开始”，也不是“已接近可玩 baseline”，而是下面这个更精确的位置：

1. Phase A 已接受，但只接受为 infrastructure foundation。
2. 旧 Phase B 任務做完了，但 objective 没有被接受；它只能算 diagnostic history。
3. Phase B-R 已证明 duration window 不再被 116 秒左右的短窗口截断，但这只是公平验证前提，不是 gameplay capability。
4. opponent model 当前只到 telemetry / response-tag 级别，没有完成 gameplay 改变，更没有完成 outcome 改善。
5. gameplay 主线仍偏薄，必须先补 build-chain、army、tactical 三段，再进入 baseline batch 与 adaptive paired evaluation。

因此，本计划的起始点是：
真实 playable core 重建期，而不是 research 扩展期。

## 三、不可违背的硬规则

### 规则 1：严格区分三条线

1. infrastructure
2. gameplay capability
3. research contribution

任何文件、任务、报告、checkpoint，必须先说明自己属于哪一类。

### 规则 2：严格区分三种状态

1. task completed：任务动作完成，例如代码改了、脚本跑了、报告写了。
2. diagnostic completed：产生了有价值的诊断或 blocker 分类，但不等于目标能力成立。
3. capability validated：目标能力在真实、公平、可追溯的条件下被验证成立。

没有 capability validated，就不能用“已完成”替代。

### 规则 3：不能再把 diagnostic completed 当成 capability validated

以下都不允许再被写成能力通过：

1. command telemetry 代替 structure ready。
2. own_army_count=0 条件下的 tactical / combat 诊断信号。
3. 被 runtime bug 或不公平窗口截断的 short run。
4. 单侧 anecdotal run 代替 paired adaptive evaluation。
5. 报告 closeout 代替 checkpoint accept。

### 规则 4：每 3 个任务必须有一个 checkpoint

本项目以任务三元组推进：

1. 实现或修复任务
2. probe / batch / paired evaluation 任务
3. checkpoint 任务

checkpoint 不通过，后续任务全部 blocked。
checkpoint 通过后，才能进入下一阶段。

### 规则 5：不允许 phase skip

1. 未过 build chain，不得跑 army core 结论。
2. 未过 army core，不得跑 tactical core 结论。
3. 未过 tactical core，不得跑 Level 1 baseline batch。
4. 未过 Level 1 baseline，不得跑 adaptive paired evaluation。
5. 未过 adaptive paired evaluation，不得宣称 research contribution 成立。

### 规则 6：debug config 不得用于 capability 或 research claim

debug 只用于 debug。
正式 gameplay claim 只允许 baseline_playable。
正式 research claim 只允许 baseline_playable 与 adaptive_research 的配对使用。

### 规则 7：repair 是主线的一部分，不是补充说明

任何 phase 失败，下一步都必须是 repair、rerun 或返回前一 phase。
不允许在 failure 未分类或未修复时继续推进下游任务。

## 四、分阶段主线

### Phase R0：研究方向与验证契约冻结

目标：
把仓库从“多个旧计划并列驱动”的状态，收束到一条新主线；同时冻结 validation protocol、config role、checkpoint discipline，保证后续 real-match evidence 不再重复旧 Phase B 的误验收。

#### Minimum

1. 研究方向决策文件落盘。
2. retain / rewrite / drop 矩阵落盘。
3. master plan 与 task queue 落盘。
4. validation protocol 落盘。
5. legacy Phase A、旧 Phase B、Phase B-R 的地位被统一重分类。

#### Target

1. debug_only、baseline_playable、adaptive_research 三类配置角色被明确冻结。
2. 评测 artifact 强制记录 code / config provenance、validation class、run class。
3. 后续执行已能只依赖新 source of truth，不再依赖旧 plan 的隐含语义。

#### Stretch

1. dry-run 入口能输出完整 provenance 与 validation class。
2. checkpoint 与报告模板可以直接复用新协议字段。

#### 必须拿到的真实证据

Phase R0 不要求新增 real SC2 evidence。
它继承的唯一真实前提是：Phase B-R 已经证明长窗口 duration probe 成立。
这个继承证据只用于证明后续 probe 具备公平运行前提，不用于证明 gameplay capability。

#### 未通过如何 repair

1. 若文档事实与仓库不一致，修正文档，不进入下一阶段。
2. 若 config role 仍不清楚，修 config contract，不进入 build-chain probe。
3. 若 evaluation artifact 仍缺 provenance，修 runner / report contract，不进入 real gameplay phase。

#### 进入下一阶段条件

checkpoint_A_start_gate 通过。

---

### Phase R1：opening build chain 可玩化

目标：
让 opening 从 command-level 诊断路径升级为 capability-level build chain，至少完成 Gateway ready 与早期 gas / cyber opportunity 的真实验证。

#### Minimum

1. Gateway ready 在有效 real probe 中被验证。
2. runtime duration 条件无争议，不能再用 short-window run 作为 build-chain 结论。
3. build stall / supply stall / gas stall / tech stall 原因可追溯。

#### Target

1. gas / cyber 路径在公平机会窗口内被验证为“已尝试并可解释”。
2. opening 结构不再依赖零散 side effect，而是具备明确 build-chain 状态。
3. 为后续 first combat-unit production 提供稳定前提。

#### Stretch

1. 在不越界宣称 army core 的前提下，出现 first combat-unit command 或 production-ready state。
2. opening build-chain 结构已能直接承接 production phase，而不是后续重写。

#### 必须拿到的真实证据

1. real match result
2. replay
3. telemetry / event summary
4. config snapshot
5. gateway command / started / ready 相关证据
6. assimilator / cyber attempt 或显式 stall classification

#### 未通过如何 repair

1. invalid evidence：原样 rerun，不改代码。
2. insufficient duration：回到 R0 修 runtime / evaluation contract，不把它误判为 gameplay failure。
3. logic failure：修 build-chain 逻辑，回 task_004。
4. prerequisite ambiguity：重写 build-chain 状态表达，不进入 R2。

#### 进入下一阶段条件

checkpoint_B_build_chain_gate 通过。

---

### Phase R2：real army production 与 rally core

目标：
在真实对局中让友军 army 确实出现，并且不是偶发现象；让 continued production 与基础 rally 成为真实 capability，而不是报告中的推定结论。

#### Minimum

1. own_army_count>0 在有效 real probe 中成立。
2. 至少一种 combat unit 被真实产出并可追溯。
3. rally 只建立在真实 army existence 上。

#### Target

1. combat-unit production 不是一次性偶发。
2. supply / gas / production idle 等阻断点被处理到足以持续生产。
3. army presence 可作为 tactical core 的可靠输入。

#### Stretch

1. first controlled move from rally 出现。
2. production path 已经能承接简单兵种构成，不必立刻引入复杂 composition。

#### 必须拿到的真实证据

1. real match artifacts 完整
2. first combat unit created
3. own_army_count transitions
4. continued production 证据
5. rally evidence 与 replay 相互印证

#### 未通过如何 repair

1. invalid evidence：rerun。
2. army 未出现：修 production，不得提前进入 tactical probe。
3. build-chain regression：回到 R1。
4. rally 逻辑不稳定：先保守固定 rally，再重新 probe。

#### 进入下一阶段条件

checkpoint_C_army_core_gate 通过。

---

### Phase R3：defend / attack transition 与 first friendly combat

目标：
在友军 army 已被验证的前提下，让 defend、attack、friendly combat 进入 capability validated，而不是停留在 enemy-visible 级别的诊断信号。

#### Minimum

1. 至少一种合法战术 order 在真实对局中成立。
2. order 发生时 own_army_count>0。
3. order 原因可解释，不能是“系统发了命令但没有 army”。

#### Target

1. friendly combat 被真实验证。
2. defend / attack 至少有一条链路可被清晰修复与稳定复现。
3. tactical probe 已足以支撑 baseline batch，不需要再靠纯战术报告推动阶段。

#### Stretch

1. defend 与 attack 两类行为都能在受控切片中观察到。
2. regroup / fallback 原因字段已经够清楚，可支持后续 baseline repair。

#### 必须拿到的真实证据

1. defend_order 或 attack_order 的 real evidence
2. friendly combat evidence
3. target_position / reason / own_army_count / enemy contact 的一致证据
4. replay 级别的可复核接敌事实

#### 未通过如何 repair

1. invalid evidence：rerun。
2. no legal tactical order：修战术逻辑，不进入 batch。
3. army regression：退回 R2。
4. 如果只出现“有敌人可见”而无友军 army 接敌，继续判为 diagnostic-only。

#### 进入下一阶段条件

checkpoint_D_tactical_core_gate 通过。

---

### Phase R4：non-adaptive baseline 的 Level 1 验收

目标：
证明 non-adaptive baseline 已经不再是 survival scaffold，而是一个可在真实 batch 中被接受的 Level 1 playable baseline。

#### Minimum

1. baseline batch 中不存在系统性 prerequisite regression。
2. baseline 的真实 gameplay 已经覆盖 build chain、army、tactical、friendly combat 基本链路。
3. 至少出现一场无争议的真正胜利或极强 near-win 证据，说明系统不再只是被动存活体。

#### Target

1. 在 protocol 规定的 easy opponent slice 上，出现重复性胜利或同等强度的稳定优势证据。
2. baseline 行为与 outcome 足以支持它作为 adaptive paired evaluation 的 control。
3. Level 1 playable baseline 被 checkpoint 正式接受。

#### Stretch

1. medium slice 产生非退化对局，可作为后续 extension 参考。
2. dominant failure class 已经收敛到少数可解释问题，而不是系统性混乱。

#### 必须拿到的真实证据

1. formal real batch artifacts
2. 完整的 provenance
3. outcome、duration、build-chain、army、tactical、combat 组合证据
4. repair 或 confirmation rerun 的对照证据
5. 显式 failure-class 排序

#### 未通过如何 repair

1. invalid evidence：原样 rerun。
2. minor instability：做一次聚焦 repair 或 confirmation，不扩 scope。
3. tactical regression：退回 R3。
4. army / production regression：退回 R2。
5. 若 batch 仍显示系统只是诊断体，禁止进入 adaptive phase。

#### 进入下一阶段条件

checkpoint_E_level1_baseline_gate 通过。
checkpoint_E 不通过，adaptive phase 不得开始。

---

### Phase R5：单一 adaptive research feature 的真实验证

目标：
在已经接受的 Level 1 baseline 上，只引入一个研究特色：稀疏侦察驱动的在线对手状态推断与时机门控层，并用 paired evaluation 验证其真实行为效应与可归因收益。

#### Minimum

1. adaptive layer 不再是 telemetry-only，而是直接控制至少一个 real gameplay gate。
2. paired evaluation 中存在可重复观察的 control vs treatment 行为差异。
3. adaptive 接入没有破坏 baseline core。

#### Target

1. 行为差异与 outcome / robustness / failure-class 改善方向一致。
2. control 与 treatment 的差异足够单一，结论可以归因到 adaptive layer。
3. checkpoint 正式接受 research contribution 成立。

#### Stretch

1. adaptive 效果在多于一个 opponent race 或 map slice 上保持同方向。
2. adaptive layer 同时稳定控制两类以上允许的时机门控，但不引入第二个 research feature。

#### 必须拿到的真实证据

1. paired real-match artifacts
2. baseline_playable 与 adaptive_research 的成对 provenance
3. continue_scouting、defensive_posture、first_attack_timing 的行为差异证据
4. outcome / failure-class 改善证据
5. paired report 中的因果解释

#### 未通过如何 repair

1. invalid evidence：rerun paired evaluation。
2. no behavior change：修 adaptive gate，不得硬写收益。
3. behavior change but no causal benefit：先冻结结论为“adaptive effect 未被接受”，再决定是否继续 repair。
4. core regression：回到 R4 通过时的 baseline control 版本，禁止带着漂移的 baseline 继续做 adaptive 结论。

#### 进入下一阶段条件

checkpoint_F_adaptive_research_gate 通过。
checkpoint_F 通过时，核心项目目标达成。
若之后要做 medium / broader-pool extension，只能作为扩展阶段，不得回写成核心目标尚未达成。

## 五、阶段之间的强依赖关系

1. R0 通过前，只能做文档、config contract、evaluation contract 工作。
2. R1 不通过，R2 blocked。
3. R2 不通过，R3 blocked。
4. R3 不通过，R4 blocked。
5. R4 不通过，R5 blocked。
6. R5 不通过，项目最多只能声称“已到 Level 1 baseline”，不能声称“已有研究贡献”。

## 六、每阶段的 minimum / target / stretch 不是同一件事

1. minimum 用来判断是否具备继续前进的资格。
2. target 用来判断该阶段是否真正达到计划目标。
3. stretch 用来决定是否可以减少后续风险或为扩展阶段铺路。

禁止把 minimum 改写成阶段最终成功定义。
禁止为了尽快通过 checkpoint，把 target 偷偷降成 minimum。
禁止把 stretch 的缺失误写为失败，但也禁止把 stretch 的偶发达成夸大为 target 稳定达成。

## 七、真实证据的统一要求

除 R0 外，每个阶段都必须至少提供以下证据包：

1. code provenance
2. config snapshot
3. match result
4. replay
5. telemetry / event summary
6. phase-specific report
7. failure-class 或 capability-validation-status 的显式记录

没有这个证据包，不能做 capability claim。
证据包不完整时，只能判为 invalid evidence 或 diagnostic-only。

## 八、repair 逻辑

### repair 的定义

repair 不是“以后再看”，而是对已发现 failure class 的直接动作。

### repair 的优先级

1. 先修 invalid evidence 与 runtime contract。
2. 再修 prerequisite regression。
3. 再修当前 phase 的主逻辑。
4. 最后才考虑更高层行为优化。

### repair 的限制

1. 一次只修 dominant failure class。
2. repair 完成后必须 rerun 与该 failure class 对应的最小必要验证。
3. 不得在 repair 中偷偷引入新 research feature。
4. 不得在 R4 之前把 baseline 与 adaptive 一起改。

## 九、checkpoint 纪律

每个 checkpoint 都必须产出以下字段，且字段必须由证据驱动：

1. reviewed_tasks
2. minimum_gate_passed
3. target_gate_passed
4. stretch_gate_status
5. evidence_paths
6. capability_validation_status
7. failure_class
8. decision
9. next_allowed_task

### checkpoint 的合法 decision

1. accepted_continue
2. repair_and_rerun
3. return_to_prior_phase
4. blocked_invalid_evidence
5. blocked_pending_prerequisite

不允许出现“看起来差不多，可以先往后跑”的非正式 decision。

## 十、哪些完成后才能进入下一阶段

1. 只有 checkpoint pass，才能 phase advance。
2. implementation task 完成但 probe 未过，不算 phase complete。
3. probe 跑完但 checkpoint 未接受，不算 phase complete。
4. report 已生成但 capability_validation_status 仍是 diagnostic-only，不算 phase complete。

## 十一、明确禁止的误推进方式

1. 用短窗口 real match 继续刷 build / combat 报告。
2. 用 debug config 继续做 capability claim。
3. baseline 未接受就把 opponent model 接入 gameplay 并开始讲研究故事。
4. 用 broader pool 或展示包装掩盖 baseline 未过关。
5. 在 mainline 未通过时，把希望寄托到 `research/` 目录里的 prototype。

## 十二、完成定义

本计划的“完成”不是“bot 能跑”，也不是“文档齐了”，而是同时满足：

1. Level 1 non-adaptive playable baseline 被 checkpoint_E 正式接受。
2. 单一 adaptive research feature 被 checkpoint_F 正式接受。
3. 两者都有真实对局证据、可追溯 artifact、明确 failure-class 语义与清晰的 control / treatment 边界。

只有这三个条件同时满足，项目才算从“基础设施 + 诊断仓库”升级为“有研究价值、可验证、可展示的 SC2 AI 项目”。
