
# 研究方向决策

状态：active
更新日期：2026-04-23
适用范围：仓库主线、计划、评测、后续 Codex 执行
取代关系：此文件与 MASTER_RESEARCH_EXECUTION_PLAN.md 一起成为主线决策源；旧路线文档保留为历史证据，不再单独决定执行优先级。

## 一句话总定位

本项目保留“单一种族 Protoss 的全游戏 StarCraft II 智能体”大方向，但立即重构为：先做出经真实对局验证的可玩核心，再围绕“稀疏侦察驱动的在线对手状态推断与时机门控”这一唯一研究特色，验证它是否能稳定改变真实行为并产生可归因收益。

## 审计后的起点

1. Phase A 已经证明的只有基础设施：真实本地对局可启动、评测流程可运行、replay / telemetry / result 可落盘、内置对手与地图池可以批量跑。
2. 旧 Phase B 没有证明 playable core。它证明的是：在被短运行窗口截断的条件下，仓库能够产生 build / combat 相关诊断信号，但没有证明 Gateway ready、Cyber Core、combat-unit production、friendly army、attack order、friendly combat、Level 1 baseline。
3. Phase B-R 目前只证明了一件事：真实对局窗口已经不再被约 116 秒上限卡死，因而后续 capability probe 具备公平机会。它没有证明 build chain、army core、combat core。
4. opponent model 当前被验证的是 telemetry 与 response-tag 通路，不是 gameplay 改变，更不是 outcome improvement。
5. 当前 gameplay 主线仍偏薄：真实行为主要由 runtime survival baseline 驱动，宏观 / 策略 / 战术管理层还没有形成一个被真实对局验收过的可玩主线。

## 主研究问题

在一个已经被真实 SC2 对局验证为可玩的 Protoss 基线之上，是否可以用稀疏 live scouting 构造一个轻量、可解释、在线更新的对手状态推断层，并让它真实改变以下三类时机门控：

1. 是否继续补侦察；
2. 是否进入防守姿态；
3. 首轮主动出击时机是否延后、保持或提前；

从而在 matched real-match evaluation 中，相比 null / non-adaptive baseline，产生可重复观察的行为差异，并在合适的对手切片上带来非偶然的结果改善。

## 当前最大问题判定

当前最大问题不是“研究方向完全错了”，也不是“再多写 telemetry 就会自然解决”，而是两件事叠加：

1. 阶段排序错误：在 playable core 未被真实验证前，项目过早投入到了 opponent-model 诊断分支。
2. 验收口径错误：task completed、diagnostic completed、capability validated 曾被混用，导致 Phase B 任务耗尽但 objective 其实没有被接受。

因此，本项目需要的不是放弃方向，而是把方向压缩为一个更硬的执行顺序：先可玩，再自适应；先 capability，再 research claim；先真实证据，再报告叙述。

## 为什么这个问题值得做

1. 它抓住了 full-game SC2 中真正有研究意味的问题：部分可观测条件下，侦察信息如何转化为可验证的实时决策改变，而不是只做静态 build order 脚本。
2. 它适合当前仓库的真实资产。仓库已经有真实对局运行、telemetry、scouting observation、null / rule-based opponent-model interface、strategy response tags 这些可直接重用的基础，但还没有大规模学习所需的数据规模和训练基础设施。
3. 它可证伪。若 adaptive layer 不改变行为、改变了行为但没有收益、或者带来收益但破坏 baseline 稳定性，结论都可以被真实对局直接否定。这比继续堆 diagnostics 更有研究价值。
4. 它保留上限。若这个轻量在线 adaptive layer 被验证有效，后续才有理由把 learned opponent model、replay learning、combat predictor 等更重模块接入主线。

## 为什么不是其他方向

### 不是“纯规则 bot 强度冲分”方向

因为那会让项目失去研究辨识度。纯强度提升可以作为阶段目标，但不能作为最终研究贡献。

### 不是“继续做 telemetry / report / diagnostic”方向

因为这条线已经超过最低可用程度。继续在没有 capability 的前提下扩写 telemetry，只会制造完成感，不会提升真实研究密度。

### 不是“直接做 AlphaStar 风格的大规模学习主线”

因为当前仓库没有经过真实验收的 baseline、没有足够规模且可靠的数据生产线、没有与该路线匹配的训练基础设施。此时转向大规模学习，只会把项目重心从研究问题转移为长期基础设施重写。

### 不是“先做 replay learning / combat predictor / SMAC micro / LLM coach”方向

因为这些都建立在已验证 playable core 之上。当前先决条件不存在，提前推进只会让主线分裂。

### 不是“先做 AI Arena / ladder 展示包装”方向

因为包装不是能力。没有已接受的 playable baseline 与 adaptive claim，展示只会放大叙事与证据的不一致。

## 项目必须围绕什么

1. 围绕真实 playable core。没有真实 build chain、army、defend / attack、friendly combat，就没有后续 adaptive research。
2. 围绕单一 research feature。只保留“稀疏侦察驱动的在线对手状态推断与时机门控层”。
3. 围绕真实对局证据。任何 gameplay 或 research claim 都必须通过 real-match protocol。
4. 围绕可归因比较。adaptive 结论必须来自 null vs adaptive 的 paired evaluation，而不是单侧 anecdotal run。
5. 围绕严格分类。任何产出必须先标明它属于 infrastructure、gameplay capability 还是 research contribution。

## 项目不得跑偏到什么

1. 不得把 diagnostic completed 写成 capability validated。
2. 不得在 Level 1 baseline 未接受前进入 Phase C / learned adaptive / broader ladder claims。
3. 不得把 telemetry richness 当成 gameplay 进步。
4. 不得同时追多个“特色”。本阶段只允许一个 research 特色，其他一律后置。
5. 不得把 multi-race、复杂 macro、扩张经济、微操炫技当成当前主线目标。
6. 不得为了“看起来像完成”而用短窗口、debug config、非对照评测去替代真实验证。

## 主研究特色只保留一个

唯一保留的主研究特色是：

稀疏侦察驱动的在线对手状态推断与时机门控层。

其定义是：

把 live scouting 形成的部分观测信息，映射为一个轻量、可解释、在线更新的 opponent state；再把这个 state 限定地作用到三类时机门控上：补侦察、防守姿态、首轮出击时机。它不是全面策略重写器，不是大模型指挥器，不是端到端策略网络，也不是新的 telemetry 展示层。

## 次要支线与后置理由

### 支线一：learned opponent model

后置原因：当前连 rule-based adaptive layer 的因果效果都未被验证，直接学习会掩盖归因问题。

### 支线二：replay / log imitation

后置原因：需要先有来自真实可玩 baseline 的高质量数据，否则学到的只是 survival scaffold。

### 支线三：combat predictor / micro module

后置原因：当前首先缺的是 army existence 与 tactical transition，不是更复杂的局部控制。

### 支线四：broader opponent pool / AI Arena / ladder packaging

后置原因：展示池应该用来放大已验证结论，而不是替代主线验证。

### 支线五：LLM coach / natural-language analysis

后置原因：它可以服务解释或工具化，但不直接构成当前 full-game SC2 主线贡献。

## 执行含义

1. Phase A 继续作为 infrastructure foundation 保留。
2. 旧 Phase B 只作为 diagnostic history 保留，不再作为 Level 1 进度依据。
3. Phase B-R 的 duration-window 修复和 checkpoint discipline 继续保留，但要并入新的 master plan，不再单独主导项目。
4. opponent model 相关资产保留接口与历史报告，但必须从 telemetry-only 改造为 gameplay gate，并且只能在 baseline accepted 之后声明研究结论。
5. 现在最值得推进的方向不是新建更多研究支线，而是完成：
   build chain -> army production -> tactical core -> baseline batch acceptance -> adaptive paired validation
   这一条唯一主线。

## 决策结论

当前方向判定为：

保留并重构。

保留的是高层目标：做全游戏 Protoss bot，并把 opponent modeling 作为真正的研究差异化来源。
重构的是执行顺序、验收口径、阶段边界和研究特色数量。
从本文件生效起，任何不服务于“真实 playable core + 单一 adaptive research feature”的工作，都不是当前主线。
