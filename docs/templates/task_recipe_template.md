
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
