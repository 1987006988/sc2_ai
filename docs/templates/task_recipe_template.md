# Task Recipe Template

状态：active
更新日期：2026-04-23
适用范围：mainline task 的具体执行 recipe
直接依赖：

* `docs/plans/active/research_master_task_queue.yaml`
* `docs/experiments/real_match_validation_protocol.md`
* `docs/experiments/checkpoint_acceptance_spec.md`
* `docs/agents/codex_execution_rules_research_mode.md`

## 第一部分：通用模板

## 1. recipe 基本信息

任务名称：
队列任务 ID：
任务分类：`infrastructure` / `gameplay capability` / `research contribution`
验证级别要求：
是否允许真实 SC2：
对应 phase：
对应 checkpoint：

## 2. 任务目的

用一句话写清本任务要回答的唯一问题。

要求：

1. 不要写成泛目标；
2. 不要同时回答两个不同层级的问题；
3. 若本任务是 real probe，目的必须是 capability claim，不是“顺便看看”。

## 3. 背景原因

写清：

1. 为什么这个任务现在必须做；
2. 它依赖前面哪个任务；
3. 它若不做，会阻塞后面哪个任务；
4. 上一次失败或 open hypothesis 是什么。

## 4. 前置检查

执行前必须逐项确认：

1. `research_master_task_queue.yaml` 中该任务就是 `active_next_task` 或 checkpoint 放行后的 `next_allowed_task`
2. `requires` 全部满足
3. 最近一个 checkpoint 没有 blocked 状态
4. 本任务的 `validation_level_required` 已理解
5. 本任务是否允许跑真实 SC2 已核对
6. 需要的 config 文件存在
7. 需要的 tests 文件存在
8. output_dir 不会覆盖不可追溯旧证据
9. 若是 paired eval，control / treatment 可比

若任一项不满足，recipe 必须 stop，不得继续。

## 5. 输入文件

列出必须打开和阅读的文件。至少要包括：

1. queue 条目
2. 本阶段计划文件
3. 本任务要修改的代码文件
4. 本任务要读取的配置文件
5. 对应的 tests
6. 若是 repair，上一轮失败报告与 artifact

## 6. 输出文件

列出本任务结束后必须产出的文件。至少要包括：

1. 修改后的代码 / 配置文件
2. 真实评测 artifact 路径
3. phase report
4. queue 更新
5. handoff 更新

## 7. 执行步骤

### 第一步做什么

写清：

1. 先开哪个文件；
2. 先核对哪个字段；
3. 先确认哪个 prerequisite。

### 第二步做什么

写清：

1. 改哪些文件；
2. 每个文件改什么；
3. 哪些字段不能动。

### 第三步做什么

写清：

1. 跑哪些测试或命令；
2. 生成哪些 artifact；
3. 到哪里检查结果。

若任务需要更多步骤，继续按第四步、第五步写，不要跳步。

## 8. 改哪些文件

按文件逐项列出：

文件路径：
修改目标：
允许改动范围：
禁止改动范围：

必须至少覆盖：

1. 代码文件
2. config 文件
3. evaluation config
4. report 文件
5. queue 与 handoff

## 9. 跑哪些命令

按顺序列出。

要求：

1. 命令必须可直接执行；
2. 先静态 / 单元测试，再 real eval；
3. 若需要生成 config，先保存文件，再跑命令；
4. 若任务不允许跑真实 SC2，不能写 real-match 命令。

## 10. 预期看到什么

按 artifact 写清：

1. `summary.json` 应该出现什么；
2. `match_result.json` 应该出现什么；
3. `events.jsonl` 应该出现什么；
4. replay 中应该看到什么；
5. 哪些信号只算 diagnostic；
6. 哪些信号才算 capability evidence。

## 11. minimum pass

写清：

1. 本任务最低算通过时必须看到什么；
2. 哪些证据缺一不可；
3. 哪些条件只要不满足就不能写 pass。

## 12. target pass

写清：

1. 本任务理想目标是什么；
2. target 比 minimum 多证明了什么；
3. target 若未达成，是否允许继续由 checkpoint 决定。

## 13. stretch

写清：

1. stretch 代表什么额外价值；
2. 没有 stretch 仍可接受；
3. 不能把 stretch 偶发达成夸大成 target。

## 14. 失败时先查什么

固定顺序建议：

1. queue 条目
2. 当前任务报告
3. `summary.json`
4. `match_result.json`
5. `telemetry/events.jsonl`
6. `replay_metadata.json`
7. `match.SC2Replay`
8. 配置文件
9. 对应代码路径

不要先拍脑袋改代码。

## 15. 如果失败如何分流

至少要分为：

1. `invalid_evidence`
2. `insufficient_duration`
3. `missing_prerequisite`
4. `logic_failure`
5. `stability_failure`
6. `no_behavior_change`
7. `regression`

并且要写清每类失败对应：

* rerun
* repair
* split
* return_to_prior_phase

## 16. 什么时候必须 stop

写清 stop 条件，例如：

1. `requires` 未满足；
2. checkpoint 未放行；
3. evidence 缺失；
4. paired 不可比；
5. 当前任务 scope 超出单轮可控；
6. prerequisite 未满足。

## 17. 什么时候必须 rerun

写清 rerun 条件，例如：

1. artifact 不完整；
2. duration 不足；
3. output_dir 污染；
4. control / treatment 一侧缺失；
5. replay / telemetry 冲突。

## 18. 什么时候必须开 repair task

写清 repair 触发条件，例如：

1. 逻辑失败已明确；
2. rerun 不会带来新信息；
3. dominant failure class 唯一明确；
4. 当前问题无法通过重新采证解决。

## 19. 完成后必须更新哪些文档

固定至少更新：

1. `docs/plans/active/research_master_task_queue.yaml`
2. `docs/handoffs/latest.md`
3. 本任务 phase report
4. 如有 checkpoint，更新 checkpoint report

## 第二部分：完整示例

以下给出一个完整、可直接使用的 recipe 示例。

任务名称：real build chain probe
队列任务 ID：`task_005_real_build_chain_probe`
任务分类：`gameplay capability`
验证级别要求：`L3`
是否允许真实 SC2：允许
对应 phase：`phase_r1_build_chain_core`
对应 checkpoint：`checkpoint_B_build_chain_gate`

## 1. 任务目的

在真实 SC2 中回答两个问题：

1. `Gateway ready` 是否在公平机会窗口内成立；
2. `Assimilator / Cybernetics Core` 的机会窗口是否被公平暴露，并能被明确分类。

本任务不回答 army、tactical、small eval 或 adaptive 问题。

## 2. 背景原因

旧 Phase B 只验证到了 gateway command 层，且曾被 116 秒左右短窗口截断。
本任务是 build-chain 真实重验证的唯一 probe。
如果本任务不能形成清晰结论，后续 production 和 army 任务都不允许开始。

## 3. 前置检查

执行前按顺序确认：

1. 打开 `docs/plans/active/research_master_task_queue.yaml`
2. 确认 `active_next_task = task_005_real_build_chain_probe`，或者最近 checkpoint 的 `next_allowed_task.on_pass = task_005_real_build_chain_probe`
3. 确认 `task_004_rebuild_opening_build_chain_logic.status = completed`
4. 确认 `task_004.actual_validation_level >= L1`
5. 确认 `configs/bot/baseline_playable.yaml` 已存在
6. 打开 `configs/bot/baseline_playable.yaml`，确认：

   * `runtime.max_game_loop` 不是 `2600`
   * `telemetry.enabled = true`
   * `telemetry.verbose = true`
   * 本文件不是 `debug.yaml`
7. 打开 `configs/evaluation/r1_build_chain_probe.yaml`，确认：

   * `evaluation.bot_config = configs/bot/baseline_playable.yaml`
   * `evaluation.launch_mode = real_launch`
   * `evaluation.output_dir = data/logs/evaluation/r1_build_chain_probe`
   * `evaluation.repeats = 1`
8. 确认 `tests/unit/test_build_progression_contract.py`、`tests/unit/test_game_loop.py`、`tests/unit/test_telemetry_schema.py` 存在
9. 若 `baseline_playable.yaml` 或 `r1_build_chain_probe.yaml` 不存在，本任务必须 stop，返回创建 config 的前序任务

## 4. 输入文件

必须先打开这些文件：

1. `docs/plans/active/research_master_task_queue.yaml`
2. `docs/experiments/real_match_validation_protocol.md`
3. `docs/plans/active/phase_playable_core_rebuild.md`
4. `configs/bot/phase_b_revalidation_gameplay.yaml`
5. `configs/bot/baseline_playable.yaml`
6. `configs/evaluation/phase_b_revalidation_duration_probe.yaml`
7. `configs/evaluation/r1_build_chain_probe.yaml`
8. `src/sc2bot/runtime/game_loop.py`
9. `src/sc2bot/config/schema.py`
10. `tests/unit/test_build_progression_contract.py`
11. `tests/unit/test_game_loop.py`
12. `tests/unit/test_telemetry_schema.py`

## 5. 输出文件

本任务结束后必须有：

1. `data/logs/evaluation/r1_build_chain_probe/summary.json`
2. `data/logs/evaluation/r1_build_chain_probe/reallaunch-*/match_result.json`
3. `data/logs/evaluation/r1_build_chain_probe/reallaunch-*/telemetry/events.jsonl`
4. `data/logs/evaluation/r1_build_chain_probe/reallaunch-*/replay_metadata.json`
5. `data/logs/evaluation/r1_build_chain_probe/reallaunch-*/match.SC2Replay`
6. `artifacts/reports/r1_build_chain_probe/report.md`
7. `docs/plans/active/research_master_task_queue.yaml` 更新
8. `docs/handoffs/latest.md` 更新

## 6. 执行步骤

### 第一步：确认 config 和 telemetry 合同

先打开：

* `configs/bot/baseline_playable.yaml`
* `configs/evaluation/r1_build_chain_probe.yaml`
* `src/sc2bot/runtime/game_loop.py`

检查并确认：

1. `baseline_playable.yaml` 的 `runtime.max_game_loop` 保持正式 long-window 值；
2. `r1_build_chain_probe.yaml` 指向 `baseline_playable.yaml`；
3. `game_loop.py` 中 build-chain telemetry 至少能提供：

   * gateway build attempt / success / failed / skipped
   * tech structure attempt / success / failed / skipped
   * reason 字段
4. 若没有任何可用的 `Gateway ready` 证据路径，先在 `game_loop.py` 中补显式 ready-count 或等价 downstream ready 证据，再继续。

不能跳过这一步。
如果连 ready 证据路径都没有，本任务最多只能产出 diagnostic-only。

### 第二步：跑静态与单元测试

按顺序执行：

1. `python -m pytest tests/unit/test_build_progression_contract.py`
2. `python -m pytest tests/unit/test_game_loop.py`
3. `python -m pytest tests/unit/test_telemetry_schema.py`

预期：

1. build progression contract 不报错；
2. game_loop 改动没有破坏现有入口；
3. telemetry schema 与当前落盘字段一致。

如果测试失败：

* stop real probe；
* 将失败归入 `rework_required` 或 `repair_and_rerun`；
* 返回 `task_004_rebuild_opening_build_chain_logic`。

### 第三步：运行 real build chain probe

执行：

`python -m evaluation.runner.run_batch --config configs/evaluation/r1_build_chain_probe.yaml`

执行后确认：

1. `data/logs/evaluation/r1_build_chain_probe/summary.json` 存在；
2. 至少有一个 `reallaunch-*` 目录；
3. 每个 `reallaunch-*` 下至少有：

   * `match_result.json`
   * `telemetry/events.jsonl`
   * `replay_metadata.json`
   * `match.SC2Replay`

若缺任一关键项，本次 probe 直接判为 `invalid_evidence`，不要继续做逻辑判断。

### 第四步：读取 artifact 并做第一轮判定

按顺序打开：

1. `summary.json`
2. `match_result.json`
3. `telemetry/events.jsonl`
4. `replay_metadata.json`
5. `match.SC2Replay`

必须检查的内容：

#### 在 `summary.json` 中确认

1. run 名称正确；
2. output_dir 正确；
3. 只包含本次 probe 的 runs；
4. 没混入旧 run。

#### 在 `match_result.json` 中确认

1. `bot_config` 指向 `configs/bot/baseline_playable.yaml`
2. 不是 `debug.yaml`
3. `requested_game_time_limit_seconds` 与 long-window probe 一致
4. 未出现明显 config drift

#### 在 `events.jsonl` 中确认

至少检查：

1. 是否有 gateway build 相关事件
2. 是否有 tech structure 相关事件
3. gateway 相关事件的 `outcome` 和 `reason`
4. 后续 tech 事件中是否出现 `gateway_ready_count > 0`
5. 是否能看到 assimilator / cyber 的 `attempt / skipped / failed / success`

#### 在 replay 中确认

1. 是否真的建成 Gateway
2. 如果 telemetry 中有 ready 证据，replay 是否支持
3. 如果 Cyber 未出现，是否因为 Gateway 根本没 ready，还是因为别的原因

### 第五步：写结论，不要越界

minimum pass 只有以下两种合法情形：

1. 有效 evidence 下，`Gateway ready` 被真实验证；
2. 有效 evidence 下，Gateway 没 ready，但 blocker classification 明确且机会窗口公平。

以下情形不算 minimum pass：

1. 只有 `build_command_issued`
2. replay 缺失
3. telemetry 缺失
4. 机会窗口不足
5. `bot_config` 漂移

target pass 需要额外满足：

1. Assimilator / Cyber 机会窗口被公平暴露；
2. `events.jsonl` 能说明是 `missing_prerequisite`、`insufficient_duration` 还是 `logic_failure`；
3. 报告中能写清下一步是 production phase 还是 repair。

stretch 仅在以下情况成立：

1. 出现 first combat-unit production-ready signal；
2. 或出现 clear handoff 说明 build chain 无需再改也可进入 production。

## 7. 每个文件改什么

### `configs/bot/baseline_playable.yaml`

必须确认或修改：

1. `bot.name`
2. `bot.strategy`
3. `runtime.max_game_loop`
4. `telemetry.enabled`
5. `telemetry.verbose`

本任务不允许改：

1. 自适应相关 treatment 字段
2. non-build-chain 的战术核心逻辑

### `configs/evaluation/r1_build_chain_probe.yaml`

必须确认或修改：

1. `evaluation.name`
2. `evaluation.bot_config`
3. `evaluation.maps_config`
4. `evaluation.opponents_config`
5. `evaluation.repeats`
6. `evaluation.output_dir`
7. `evaluation.run_id`
8. `evaluation.isolate_runs`
9. `evaluation.fail_on_crash`

### `src/sc2bot/runtime/game_loop.py`

本任务允许修改：

1. build-chain telemetry contract
2. ready evidence path
3. build-chain reason 字段

本任务不允许修改：

1. tactical research logic
2. adaptive behavior
3. broader refactor

### `artifacts/reports/r1_build_chain_probe/report.md`

必须写出：

1. config provenance
2. artifact completeness
3. actual game time sufficiency
4. gateway ready verdict
5. assimilator / cyber verdict
6. capability_validation_status
7. failure_class
8. next step

### `docs/plans/active/research_master_task_queue.yaml`

必须更新：

1. `task_005.status`
2. `task_005.actual_validation_level`
3. `task_005.real_validation_status`
4. `task_005.evidence_paths`
5. `task_005.capability_validation_status`

### `docs/handoffs/latest.md`

必须更新：

1. 当前任务名称
2. 本轮 probe 的 artifact 路径
3. minimum / target 结论
4. 若失败，dominant failure class
5. 下一允许任务

## 8. 预期看到什么

### minimum pass 预期

1. `summary.json` 存在
2. `match_result.json` 指向 `baseline_playable.yaml`
3. `events.jsonl` 里至少有完整 gateway build 事件链
4. `Gateway ready` 有明确证据，或者 blocker classification 无歧义
5. replay 与 telemetry 不冲突

### target pass 预期

1. `gateway_ready_count > 0` 已被看到，或 replay 明确支持 Gateway completed
2. `Assimilator` 和 `Cybernetics Core` 的机会被公平暴露
3. 原因链可清楚区分：

   * `insufficient_duration`
   * `missing_prerequisite`
   * `build_chain_logic_failure`

### stretch 预期

1. 后续出现 production-ready signal
2. build chain 报告足以直接支持进入 P2 / P3

## 9. 失败时先查什么

按以下顺序，不要跳：

1. queue 中 `task_005.requires` 是否满足
2. `summary.json`
3. `match_result.json` 的 `bot_config`
4. `events.jsonl` 是否完整
5. replay 是否存在
6. `baseline_playable.yaml` 是否被误改
7. `game_loop.py` 是否根本没输出 ready-compatible evidence

## 10. 如果失败如何分流

### 情形 A：artifact 缺失

分类：
`invalid_evidence`

动作：
原样 rerun `task_005_real_build_chain_probe`

### 情形 B：actual game time 不足

分类：
`insufficient_duration`

动作：
返回配置 / runtime 合同修复，不要判逻辑失败

### 情形 C：只有 gateway command，没有 ready

若 evidence 不足：
`telemetry_contract_gap`

动作：
先补 ready evidence path，再 rerun

若 evidence 完整但仍不 ready：
`build_chain_logic_failure`

动作：
返回 `task_004_rebuild_opening_build_chain_logic`

### 情形 D：Gateway ready 已经成立，但 Assimilator / Cyber 仍不出现

分类：
`missing_prerequisite` 或 `build_chain_logic_failure`

动作：
返回 `task_004_rebuild_opening_build_chain_logic`

## 11. 什么时候必须 stop

1. `task_004` 未完成
2. `baseline_playable.yaml` 不存在
3. `r1_build_chain_probe.yaml` 指向错误 bot config
4. unit tests 没过
5. artifact 缺失但尚未 rerun
6. actual game time 不足但你还想下 gameplay 结论

## 12. 什么时候必须 rerun

1. `summary.json` 缺失
2. replay 缺失
3. `match_result.json` 指向错误 config
4. output_dir 混入旧 run
5. 只有 evidence 问题，没有新逻辑信息

## 13. 什么时候必须开 repair task

1. `Gateway ready` 持续不成立；
2. `gateway_ready_count` 证据路径缺失；
3. `Assimilator / Cyber` 在公平窗口内持续不出现；
4. rerun 后仍无法区分 prereq 与 logic failure。

repair 入口固定为：

* `task_004_rebuild_opening_build_chain_logic`

## 14. 完成后必须更新哪些文档

1. `docs/plans/active/research_master_task_queue.yaml`
2. `docs/handoffs/latest.md`
3. `artifacts/reports/r1_build_chain_probe/report.md`

若本任务是 checkpoint 前的验证任务，不得在本 recipe 中直接把下一阶段改成可执行；必须等 `checkpoint_B_build_chain_gate` 决定。
