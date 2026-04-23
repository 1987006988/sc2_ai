
# 保留 / 重写 / 后置 / 停止矩阵

状态：active
更新日期：2026-04-23
适用范围：仓库现有资产的主线处置
使用方式：任何计划调整、代码重构、评测设计、报告生成，都先参照本矩阵决定某类资产属于“保留”“重写”“后置”还是“停止”。

## 处置原则

1. 保留：该资产已经为主线提供真实基础，不应推倒重来。
2. 重写：该资产包含有用事实，但当前叙事、接口、职责或验收方式不适合继续直接使用。
3. 后置：该资产方向并非错误，但不应早于 playable core 与 Level 1 baseline。
4. 停止：该资产继续推进只会制造完成感、放大误验收，或对当前主线构成噪声。

---

## 一、Phase A 资产

当前判定：保留为 infrastructure foundation；重写其对外表述；停止把其用于 gameplay 或 research claim。

### 可保留

1. real-match launch、SC2PATH 预检、map / opponent pool、artifact persistence、batch orchestration 相关实现与数据。
2. `artifacts/reports/phase_a_ladder_infra_dataset/` 下的基础设施报告与 manifest。
3. `docs/context/validated_findings.md` 中与本地真实运行、replay 保存、地图安装、评测落盘有关的事实。
4. Phase A 对 real-match-first discipline 的基础实践。

### 需要重写

1. 所有让人误以为 Phase A 代表 gameplay progress 的叙述。
2. README 与 active plan 中对 Phase A 成果的上下文定位。
3. 后续报告模板中对 Phase A 数据的引用方式，必须显式标记为 infrastructure-only。

### 应后置

1. 以 Phase A 数据为起点做更大规模的数据集美化、统计可视化、展示包装。
2. 任何把 Phase A baseline dataset 直接接到学习分支的工作。

### 应停止

1. 用 Phase A 的 artifact 完整性去暗示 bot 已经 playable。
2. 在没有新 capability evidence 的前提下继续扩写 Phase A 风格的基础设施报告。

### 保留原因

Phase A 解决的是“能不能稳定跑真实 SC2 并拿到可审计 artifact”这个基础问题，这一层已经是仓库最扎实的已验证资产，不应被推翻。

### 重写原因

Phase A 的问题不在事实，而在叙事风险。若不重写表述，它会被误读成“项目已经接近 gameplay baseline”，这与仓库现状不符。

### 风险

1. 基础设施完成感掩盖 gameplay 缺口。
2. Phase A dataset 被错误复用为可玩性证据。
3. 资源继续投入到报表而不是核心能力。

### 迁移建议

1. 把 Phase A 永久标记为 infrastructure foundation。
2. 在所有新报告中单独列出“继承自 Phase A 的基础设施能力”，不得与 gameplay evidence 混写。
3. 保留数据与实现，不再给 Phase A 新建主线里程碑。

---

## 二、旧 Phase B 资产

当前判定：保留 raw evidence 与 evidence audit；重写其主计划地位；停止把旧 Phase B 当作 Level 1 进度。

### 可保留

1. `artifacts/reports/phase_b_playable_competitive_core/evidence_audit.md`。
2. 旧 Phase B real-match artifacts、replays、telemetry、small-eval 原始输出。
3. 旧 Phase B 中关于 capability vs diagnostic 的重新分类结果。
4. 对 runtime duration bug 的定位结果及其历史链路。

### 需要重写

1. `docs/plans/active/phase_b_playable_competitive_core.md` 的主线地位。
2. 旧 Phase B task queue 在主项目中的使用方式。
3. 任何把旧 Phase B “任务完成”叙述成“playable core 已通过”的报告或 README 文案。

### 应后置

1. 对旧 Phase B 数据再做新的总结性图表、美化版报告。
2. 基于旧 Phase B small eval 做对外展示。

### 应停止

1. 把旧 Phase B 的 gateway command telemetry 当成 gateway-ready。
2. 把 own_army_count=0 条件下的 attack / defend / combat 诊断信号当成真实 army capability。
3. 把旧 Phase B 小规模 batch 当成 Level 1 baseline。

### 保留原因

旧 Phase B 虽然没完成原目标，但它非常有价值地证明了哪里没有被验证、为什么没有被验证、以及为什么后续必须改验收口径。

### 重写原因

旧 Phase B 的最大问题不是没有数据，而是任务目标、完成状态与能力状态之间的映射失真。主线必须改成“历史诊断资产”，不能继续作为现行成功依据。

### 风险

1. 继续误用 legacy evidence，导致后续 checkpoint 被污染。
2. 让团队误以为“再补几份报告就能过关”。
3. 让 adaptive 研究建立在未验证 baseline 之上。

### 迁移建议

1. 旧 Phase B 文档全部标记为 legacy diagnostic path。
2. 保留 evidence audit 作为失败分类样板。
3. 在新主计划中只引用旧 Phase B 的 blocker、failure class、raw evidence，不再引用其 closeout 叙述。

---

## 三、Phase B-R 资产

当前判定：保留 duration-window 修复证据与 checkpoint discipline；重写其边界与归属；后置其作为单独阶段文档的主导地位。

### 可保留

1. `docs/handoffs/latest.md` 中关于 real duration probe 的事实。
2. `docs/plans/active/phase_b_revalidation_playable_core.md` 中对严格验收、failure class、minimum / target / stretch 的设计。
3. `docs/plans/active/phase_b_revalidation_task_queue.yaml` 中“每 3 个任务一个 checkpoint”的纪律。
4. `configs/bot/phase_b_revalidation_gameplay.yaml` 作为过渡期长窗口 gameplay config 的参考。
5. Duration probe 的 raw artifacts。

### 需要重写

1. Phase B-R 作为“独立主线阶段”的定位。
2. 其 task queue 与新的 master queue 的关系。
3. handoff 中“已完成”叙事的解释边界，必须明确它只证明 duration 公平性。

### 应后置

1. 把 Phase B-R 文档继续扩成一条长期独立路线。
2. 在没有 master plan 收编前继续追加 Phase B-R 风格局部任务。

### 应停止

1. 把 duration-window probe 解释成 build-chain、army core、combat core 已恢复。
2. 让 Phase B-R 继续以旧 Phase B 语义独自推进，而不受新的全局计划统一调度。

### 保留原因

Phase B-R 引入了两个对主线非常重要的资产：一是公平运行窗口的修复事实，二是 checkpoint / gate / failure-class 的执行纪律。

### 重写原因

Phase B-R 仍然过于局部，只解决了“如何重新验证旧 Phase B”的问题，而没有成为“如何完成真实 playable core 并过渡到 research claim”的总框架。

### 风险

1. 项目长期停留在“局部 revalidation”而无法进入 research contribution 阶段。
2. queue 与 active plan 并行失控。
3. 继续以 Phase B 思维理解更大主线。

### 迁移建议

1. 把 Phase B-R 的 duration repair、gate discipline、failure taxonomy 吸收进新 master plan 与 validation protocol。
2. 旧 Phase B-R 文件保留只读历史地位。
3. 后续执行统一由 `MASTER_RESEARCH_EXECUTION_PLAN.md` 与 `research_master_task_queue.yaml` 驱动。

---

## 四、opponent model 相关资产

当前判定：保留接口、null / rule-based 基线与历史 ablation；重写目标与验收；后置 learned opponent model；停止把 telemetry-only 路径叫做 adaptive bot。

### 可保留

1. `src/sc2bot/opponent_model/` 下的 interface、null model、rule-based model。
2. `src/sc2bot/managers/strategy_manager.py` 中的 response-tag 选择骨架。
3. `artifacts/reports/phase1d_ablation_opponent_model/` 与 `artifacts/reports/phase1e_strategy_intervention/` 的历史报告。
4. scouting observation、opponent prediction、strategy response 这条数据通路。

### 需要重写

1. opponent model 的主目标：从“能产生 prediction / tag”改为“能真实改变 gameplay gate 并接受 paired evaluation”。
2. strategy response 的作用范围：必须直连 gameplay，而不是只记 telemetry。
3. adaptive claim 的验收口径：必须从单侧运行改为 control vs treatment 的 paired evaluation。

### 应后置

1. learned opponent model。
2. replay-driven hidden-state estimator。
3. 更复杂的多分支 response policy。
4. broader opponent pool 上的 adaptive generalization 叙述。

### 应停止

1. 用 prediction telemetry 丰富度代替 adaptive 成功。
2. 在 baseline 未接受前继续扩 opponent-model 规则集。
3. 把 Phase1D / Phase1E 报告解读为 outcome improvement 证据。

### 保留原因

当前 opponent model 相关资产已经把“观测 -> 预测 -> response tag”的接口链条打通了，这为单一 adaptive research feature 提供了直接可用的骨架。

### 重写原因

当前问题不是接口没有，而是它没有对 gameplay 产生经验证的因果作用。必须把它从“说明系统有这条通路”升级为“说明这条通路真的改变行为并带来收益”。

### 风险

1. 继续沉迷于 prediction telemetry，重复 Phase1D / Phase1E 的问题。
2. 提前引入 learned model，掩盖主线可解释性与归因。
3. adaptive claim 与 baseline stability 同时漂移，导致 paired evaluation 不可比。

### 迁移建议

1. 保留 interface，不改 mainline / research 分隔原则。
2. 只保留一个 adaptive feature：对 continue_scouting、defensive_posture、first_attack_timing 的门控。
3. 所有 adaptive 代码必须在 Level 1 baseline accepted 之后进入主线验证。

---

## 五、telemetry / report 相关资产

当前判定：保留 telemetry schema、artifact persistence、报告生成骨架；重写报告分类与验证语义；后置展示型报表；停止 telemetry-only milestone。

### 可保留

1. 当前 telemetry 输出与 event persistence 管线。
2. `artifacts/reports/` 下已经能自动整理的基本报告框架。
3. match_result、replay、telemetry summary、manifest 这些 artifact 组织方式。
4. evidence audit 这种“先分类再下结论”的写法。

### 需要重写

1. 所有报告模板必须强制分离：

   * infrastructure
   * gameplay capability
   * research contribution
2. 每个报告必须显式写明：

   * task completed status
   * diagnostic completed status
   * capability validation status
3. checkpoint 报告必须写 failure class、decision、next allowed task。

### 应后置

1. 仪表盘美化。
2. 大规模可视化。
3. 对外展示用叙述性长报告。

### 应停止

1. 以“事件更多了、报表更丰富了”充当能力进度。
2. 在 capability 未过关时追加纯 telemetry 任务。
3. 用报告 closeout 语言替代 checkpoint 审核。

### 保留原因

telemetry 和报告基础设施不是问题来源，它们反而是当前仓库最成熟的证据管道之一。

### 重写原因

问题出在报告如何解释证据、如何分类、如何影响决策。报告必须回到服务 gate，而不是制造叙事完成度。

### 风险

1. 指标膨胀，掩盖能力空洞。
2. 报告语言继续领先于证据。
3. 执行资源被报表工作吞噬。

### 迁移建议

1. 后续所有报告都以 `real_match_validation_protocol.md` 为分类准绳。
2. checkpoint 报告成为唯一可改变队列状态的报告。
3. 非 checkpoint 报告不得单独宣布 phase accepted。

---

## 六、runtime / config 相关资产

当前判定：保留 real launch、runner、SC2PATH preflight、长窗口 gameplay config；重写配置角色与 gameplay ownership；后置大型框架重构；停止用 debug config 做 capability eval。

### 可保留

1. `src/sc2bot/runtime/` 下的真实运行入口。
2. 现有 evaluation runner、SC2PATH 处理、地图检查、real local match orchestration。
3. `configs/bot/phase_b_revalidation_gameplay.yaml` 作为长窗口 gameplay config 参考。
4. 现有 build-order 参数接口与 runtime.max_game_loop 相关配置能力。

### 需要重写

1. `debug.yaml` 的角色定义，必须明确为 debug_only。
2. baseline_playable 与 adaptive_research 两类正式评测配置。
3. gameplay ownership。当前大量真实行为仍在 runtime survival baseline 中，macro manager 仍过于空壳，必须至少收敛为可维护的 build / army / tactical 主线。
4. provenance 记录：任何真实评测都必须保存 code / config snapshot。

### 应后置

1. 为了“架构漂亮”而做的大型框架重写。
2. 与当前主线无关的配置拆分、参数中心化或复杂 profile 系统。

### 应停止

1. 用 `configs/bot/debug.yaml` 做 capability claim 或 research claim。
2. 继续让短窗口或隐式窗口控制混入正式评测。
3. 在 gameplay ownership 未理顺前同时重写多层 manager 和 runtime。

### 保留原因

runtime / evaluation 层已经证明能够真实启动、持续运行并落盘 artifact。真正的问题不是没有运行层，而是 gameplay 逻辑组织与配置角色混乱。

### 重写原因

如果不明确 debug_only、baseline_playable、adaptive_research 三类配置角色，旧 Phase B 的验收事故会重复发生。

### 风险

1. 同一能力在不同配置下得出不可比结论。
2. gameplay 代码继续散落，难以形成 build-chain / army / tactical 的可靠修复闭环。
3. 大型架构重写拖垮主线节奏。

### 迁移建议

1. 先做“足够支撑主线”的重构，不做“为了整洁”的全面重构。
2. 以 build-chain -> army -> tactical 三段为轴心收拢 gameplay ownership。
3. 正式评测只允许 baseline_playable 与 adaptive_research 两条配置主线。

---

## 七、research 相关资产

当前判定：保留 `research/` 目录作为隔离区；后置绝大多数 prototype；停止把 research prototype 当 mainline 进度。

### 可保留

1. `research/` 目录及其“与 mainline 隔离”的仓库约定。
2. 与 replay learning、combat predictor、smac_micro、llm_coach 等相关的原型探索价值。
3. AGENTS 中关于 mainline 与 research 分隔的规则。

### 需要重写

1. prototype promotion 条件。
2. prototype 何时允许进入主线的验收标准。
3. 研究型分支与当前唯一主研究特色之间的优先级关系。

### 应后置

1. replay learning
2. combat predictor
3. smac_micro
4. llm_coach
5. 更重的 learned opponent modeling

### 应停止

1. 在 playable core 未接受前把 research prototype 接入主线。
2. 用 prototype 存在本身去证明项目“接近前沿”。
3. 在没有 paired evaluation 证据前宣称研究贡献成立。

### 保留原因

`research/` 目录本身没有问题；问题是它与当前主线的时序关系。隔离区让仓库可以保留想法，但不污染 mainline。

### 重写原因

必须把“何时允许进入主线”从模糊意愿改成硬门槛：只有当 playable baseline 被接受、且 prototype 服务于当前唯一研究特色时，才允许 promotion。

### 风险

1. 研究支线过早分裂主线。
2. prototype 质量与 mainline 质量互相拖累。
3. 项目叙事漂向“什么都在做”，但没有一个真实结论完成。

### 迁移建议

1. 保留 research 目录，不迁入 `src/sc2bot/`。
2. 所有 prototype promotion 先过 two-step gate：

   * Level 1 baseline accepted
   * paired adaptive evaluation 需要它
3. 当前阶段一律不把 `research/` 目录作为主线输出依据。

---

## 八、README / docs 相关资产

当前判定：保留 AGENTS 与 context 文档中的事实价值；重写 README、active plan、状态叙述；后置对外包装；停止使用过时路线文档作为 source of truth。

### 可保留

1. `AGENTS.md` 中关于 mainline / research 分隔、promotion 纪律、计划优先级的基本约束。
2. `docs/context/current_status.md`、`validated_findings.md`、`open_hypotheses.md` 中的事实性内容。
3. `docs/handoffs/latest.md` 的交接机制本身。
4. 现有 plan 文档作为历史路径记录。

### 需要重写

1. `README.md` 的当前主线叙述。
2. `docs/plans/active/ladder_competitive_adaptive_sc2_bot_plan.md` 的 source-of-truth 地位。
3. 所有 still-active 但已与仓库现状不一致的 next step、phase status、closeout 说明。
4. docs 中对 Phase A / Phase B / Phase B-R 的关系叙述。

### 应后置

1. 对外展示型 README 强化。
2. 对 broader pool、AI Arena、showcase 的文案打磨。

### 应停止

1. 继续让多个 active plan 并列充当主计划。
2. 在 README 里用“长期目标”掩盖当前 baseline 真实状态。
3. 让 handoff 文档绕开 master queue 直接定义下一任务。

### 保留原因

当前 docs 系统已经累积了大量事实与过程记录，不应推倒。真正的问题在于哪些文档是历史，哪些文档是现行指令。

### 重写原因

如果 source of truth 不收敛，Codex 后续执行会被旧 plan、旧 closeout、旧 handoff 同时拉扯。

### 风险

1. 文档互相矛盾。
2. 新执行者误读项目真实进度。
3. 同一能力在不同文档中被定义成不同东西。

### 迁移建议

1. 从本轮开始，以下文件组成新的执行真源：

   * `docs/foundation/04_research_direction/research_direction_decision.md`
   * `docs/foundation/04_research_direction/retain_rewrite_drop_matrix.md`
   * `docs/plans/active/MASTER_RESEARCH_EXECUTION_PLAN.md`
   * `docs/plans/active/research_master_task_queue.yaml`
   * `docs/experiments/real_match_validation_protocol.md`
2. 旧 active plan 保留为历史背景，但不再单独驱动任务。
3. 所有 handoff 都必须引用 master queue 的当前任务与 checkpoint 状态。

---

## 统一迁移规则

1. 历史 artifacts 不删除，只重分类。
2. source of truth 只允许一个集合，不允许多条 active 主计划并行。
3. 任何资产若无法明确归类为 infrastructure、gameplay capability、research contribution，就不得进入新阶段 gate。
4. 任何继续推进 telemetry-only、report-only、prototype-only 而不服务于 playable core 或单一 adaptive research feature 的工作，都视为停止项。
