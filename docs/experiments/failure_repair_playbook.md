
# Failure Repair Playbook

状态：active
更新日期：2026-04-23
适用范围：playable core 与 adaptive response 阶段的失败排查、修复和重跑
直接依赖：

* `docs/plans/active/research_master_task_queue.yaml`
* `docs/plans/active/phase_playable_core_rebuild.md`
* `docs/plans/active/phase_adaptive_response_research.md`
* `docs/experiments/real_match_validation_protocol.md`
* `docs/experiments/checkpoint_acceptance_spec.md`

## 1. 使用规则

每次失败都先按以下顺序处理，不允许直接拍脑袋修代码：

1. 先判 evidence 是否有效；
2. 再判 actual game time 是否足够；
3. 再判 prerequisite 是否满足；
4. 最后才判 logic failure。

任何 repair 都只修一个 dominant failure class。
任何 repair 之后都必须回到最小必要验证单元重跑。
若 repair 后发现 prior phase prerequisite 回归，立即回 prior phase，不要继续当前 phase。

## 2. repair task 对照表

* build chain 类问题：回 `task_004_rebuild_opening_build_chain_logic`
* duration / config 合同问题：回 `task_002_lock_runtime_eval_contract_and_config_roles`
* production / army 类问题：回 `task_007_rewrite_combat_unit_production_and_rally_logic`
* tactical / friendly combat 类问题：回 `task_010_rewrite_defend_attack_transition_logic`
* baseline batch 稳定性问题：回 `task_014_baseline_repair_or_confirmation`
* adaptive gate 问题：回 `task_016_integrate_single_adaptive_gating_layer`
* paired eval 可比性或证据问题：回 `task_017_null_vs_adaptive_paired_evaluation`

## 3. Failure Case 1：对局窗口不足

### 现象

1. run 很早结束；
2. key claim 还没到最小公平机会窗口；
3. 旧式短窗口症状再次出现；
4. build / combat / paired 结论都说不清。

### 常见原因

1. `bot_config` 实际仍指向 `debug.yaml`
2. `runtime.max_game_loop` 被错误改回低值
3. evaluation config 指错 bot config
4. control / treatment 其中一侧持续时间不足
5. output_dir 混乱，误读了旧 run

### 先查哪些 artifact

1. `summary.json`
2. `match_result.json`
3. `replay_metadata.json`
4. `preflight.json`
5. `launch_path_diagnostics.json`（若存在）

### 再查哪些配置

1. `configs/bot/debug.yaml`
2. `configs/bot/baseline_playable.yaml`
3. `configs/bot/adaptive_research.yaml`
4. 当前 `configs/evaluation/*.yaml`

重点检查：

* `runtime.max_game_loop`
* `evaluation.bot_config`
* `evaluation.output_dir`
* `evaluation.run_id`

### 再查哪些代码路径

1. `src/sc2bot/runtime/game_loop.py`
2. `evaluation/runner/run_match.py`
3. `src/sc2bot/config/schema.py`

### 如何区分

* 若 artifact 缺失或配置指错：`invalid_evidence`
* 若 artifact 完整，但在公平机会窗口前正常结束：`insufficient_duration`
* 若时间足够却仍无进展：继续查 prerequisite 或 logic
* 若 paired 一侧足够一侧不足：paired `invalid_evidence` 或 `insufficient_duration`

### 修复动作

1. 修 evaluation config 指向
2. 修 `baseline_playable.yaml` / `adaptive_research.yaml` 的 `runtime.max_game_loop`
3. 清理错误 output_dir 或换新 run_id
4. 不改 gameplay 代码，除非已确认退出逻辑本身有 bug

### 修复后必须重跑哪一步

* 原 task 的同级 probe / batch / paired eval

### 重跑仍失败时转向

* `task_002_lock_runtime_eval_contract_and_config_roles`
* 不允许继续当前 gameplay / research phase

## 4. Failure Case 2：Gateway command 有但 Gateway-ready 没有

### 现象

1. `events.jsonl` 中有 gateway build attempt 或 success
2. replay 或下游事件里看不到 Gateway ready
3. report 只能说 command 发过了

### 常见原因

1. 只记录了 command telemetry，没有 ready 证据路径
2. Pylon / probe / resource prerequisite 不稳
3. 建造位置失败或异常
4. run 结束得太早，Gateway 还没建完
5. build chain 逻辑重复发命令但没进入稳定完成状态

### 先查哪些 artifact

1. `summary.json`
2. `match_result.json`
3. `telemetry/events.jsonl`
4. `match.SC2Replay`

重点查：

* gateway build 事件的 `outcome`
* gateway build 事件的 `reason`
* 后续 tech 事件是否包含 `gateway_ready_count > 0`

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.gateway_min_probe_count`
* `build_order.gateway_min_game_time`
* `build_order.pylon_supply_buffer`
* `runtime.worker_gather`
* `runtime.supply_sustain`

### 再查哪些代码路径

1. `src/sc2bot/runtime/game_loop.py`

   * `_safe_gateway_build`
   * `_record_gateway_build`
2. 与 gateway skip reason 相关逻辑
3. 若 build chain 已抽取 helper，则查对应 helper

### 如何区分

* 若 run 在完成前结束：`insufficient_duration`
* 若没有 Pylon / 资源 / probe 前置：`missing_prerequisite`
* 若 command 成功但 ready 始终无从确认：`telemetry_contract_gap`
* 若 command 反复发出但结构始终没稳定完成：`build_chain_logic_failure`
* 若 replay 缺失：`invalid_evidence`

### 修复动作

1. 若是 evidence gap，先补 `Gateway ready` 证据路径
2. 若是前置问题，修 build-chain prerequisite
3. 若是 placement / exception，修 build 逻辑和错误处理
4. 不允许直接把 command 当 ready

### 修复后必须重跑哪一步

* `task_005_real_build_chain_probe`

### 重跑仍失败时转向

* `task_004_rebuild_opening_build_chain_logic`

## 5. Failure Case 3：Cyber Core 不出现

### 现象

1. Gateway 似乎已经有进展；
2. `Cybernetics Core` 相关事件始终没有成功；
3. 生产链停在 gas / cyber 之前。

### 常见原因

1. Gateway 其实没 ready
2. Assimilator 没建成或 gas 不可用
3. `cybernetics_core_enabled = false`
4. 资源或建造位置不足
5. run 只够看到 gateway，不够看到 cyber

### 先查哪些 artifact

1. `telemetry/events.jsonl`
2. `match.SC2Replay`
3. `match_result.json`

重点查：

* `tech_structure_build` 中 `structure_name = assimilator`
* `tech_structure_build` 中 `structure_name = cybernetics_core`
* `gateway_ready_count`
* `pending_count`
* `existing_count`
* `reason`

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.assimilator_enabled`
* `build_order.cybernetics_core_enabled`
* `runtime.worker_gather`
* `runtime.supply_sustain`

### 再查哪些代码路径

1. `src/sc2bot/runtime/game_loop.py`

   * `_safe_assimilator_build`
   * `_safe_cybernetics_core_build`
   * `_record_tech_structure_build`

### 如何区分

* `gateway_ready_count = 0`：`missing_prerequisite`
* run 在 cyber 公平机会前结束：`insufficient_duration`
* evidence 缺失：`invalid_evidence`
* 条件满足但仍反复失败：`build_chain_logic_failure`

### 修复动作

1. 若 Gateway 未 ready，先回 Gateway 问题，不要直接修 cyber
2. 若 Assimilator 未建成，先修 gas 路径
3. 若 config 关闭了 cyber，修 config
4. 若 logic 明显错误，修 `_safe_cybernetics_core_build`

### 修复后必须重跑哪一步

* `task_005_real_build_chain_probe`

### 重跑仍失败时转向

* `task_004_rebuild_opening_build_chain_logic`

## 6. Failure Case 4：Zealot / Stalker 不出现

### 现象

1. `combat_unit_production` 有 attempt 或 success
2. replay 中却看不到对应战斗单位
3. `own_army_count` 没增长

### 常见原因

1. 只有 `train_command_issued`，没有 unit created
2. `idle_gateway_count = 0`
3. `gateway_ready_count = 0`
4. `cybernetics_core_ready_count = 0`，导致 stalker 不可生产
5. supply block 或资源不足
6. unit type 配置不支持

### 先查哪些 artifact

1. `telemetry/events.jsonl`
2. `match.SC2Replay`
3. `match_result.json`

重点查 `combat_unit_production` 事件中的：

* `outcome`
* `reason`
* `unit_name`
* `gateway_ready_count`
* `cybernetics_core_ready_count`
* `idle_gateway_count`

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.zealot_production_priority`
* `build_order.stalker_production_priority`
* `runtime.supply_sustain`
* `runtime.supply_sustain_threshold`

### 再查哪些代码路径

1. `src/sc2bot/runtime/game_loop.py`

   * `_safe_combat_unit_production`
   * `_combat_unit_type`
   * `_record_combat_unit_production`

### 如何区分

* 若 `gateway_ready_count = 0`：前置问题，回 build chain
* 若 `cybernetics_core_ready_count = 0` 且 unit 是 stalker：前置问题
* 若 `idle_gateway_count = 0`：生产逻辑 / 调度问题
* 若 `cannot_afford_unit`：资源或经济前置问题
* 若 replay 缺失：`invalid_evidence`
* 若 run 过短：`insufficient_duration`

### 修复动作

1. 先确认单位真实出现的证据路径，不要只盯着 `train_command_issued`
2. 解决 idle gateway、资源、tech prerequisite
3. 若只需要最小 playable baseline，优先保证最容易稳定出现的第一批单位
4. 不要在这里引入复杂 composition 系统

### 修复后必须重跑哪一步

* 先重跑 `task_008_real_army_presence_probe`

### 重跑仍失败时转向

* `task_007_rewrite_combat_unit_production_and_rally_logic`
* 若 tech prerequisite 回归，则回 `task_004`

## 7. Failure Case 5：own_army_count 一直为 0

### 现象

1. 生产链似乎在运行；
2. report 却始终显示 `own_army_count = 0`；
3. tactical probe 因无 army 无法成立。

### 常见原因

1. 生产实际上没成功
2. unit 出现了，但 state extraction 错
3. unit 刚出现就死亡
4. run 还没到 army 出现窗口
5. replay 存在，但 telemetry 对不上

### 先查哪些 artifact

1. `telemetry/events.jsonl`
2. `match.SC2Replay`
3. `summary.json`

重点看：

* `combat_unit_production`
* `game_state`
* `army_order`
* replay 中是否确有友军战斗单位

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.zealot_production_priority`
* `build_order.stalker_production_priority`
* `runtime.army_defense`
* supply / gather 相关字段

### 再查哪些代码路径

1. `src/sc2bot/runtime/game_loop.py`
2. `src/sc2bot/domain/game_state.py`
3. `build_game_state_from_bot_ai` 或等价 state 构建路径

### 如何区分

* replay 中无单位：生产失败，`production_logic_failure`
* replay 中有单位，telemetry 仍为 0：`state_extraction_failure`
* replay 中有单位但立即死亡：可能是 `tactical` 或 `positioning` 问题
* run 太短：`insufficient_duration`
* artifact 缺失：`invalid_evidence`

### 修复动作

1. 先确认问题是“单位没生成”还是“计数没记录”
2. 如果是 state extraction 错，先修 extraction，不要直接改 tactical
3. 如果单位出现但立即死，先看 rally / positioning，再考虑 tactical

### 修复后必须重跑哪一步

* `task_008_real_army_presence_probe`

### 重跑仍失败时转向

* `task_007_rewrite_combat_unit_production_and_rally_logic`
* 若发现 opening 回归，则回 `task_004`

## 8. Failure Case 6：attack / defend order 没有

### 现象

1. army 已存在；
2. `attack_order` 和 `defend_order` 始终不出现；
3. tactical probe 没法形成正结论。

### 常见原因

1. `attack_army_supply_threshold` 或 `attack_game_time_threshold` 太高
2. `known_enemy_start_location` 不可用
3. defend 触发条件过严
4. `tactical_manager.py` 只会返回 rally
5. `game_loop.py` 没把 tactical plan 接到真实执行

### 先查哪些 artifact

1. `telemetry/events.jsonl`
2. `match.SC2Replay`

重点查：

* `army_order`
* `game_state`
* `combat_event_skipped`
* `strategy_response`（如果战术门控已接入）

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.attack_army_supply_threshold`
* `build_order.attack_game_time_threshold`
* `build_order.defend_radius`
* `runtime.army_defense`

### 再查哪些代码路径

1. `src/sc2bot/managers/tactical_manager.py`
2. `src/sc2bot/runtime/game_loop.py`

### 如何区分

* `own_army_count = 0`：不是 tactical 问题，是 prior phase prerequisite
* army 有，enemy location 无：可能是 scouting / known enemy location 问题
* army 有，阈值永远达不到：`config_threshold_mismatch`
* army 有，条件满足但仍无 order：`tactical_logic_failure`
* evidence 缺失：`invalid_evidence`

### 修复动作

1. 先把 `own_army_count` prerequisite 问题排除
2. 再调 tactical threshold 和 reason logic
3. 确保 `reason` 被落盘
4. 不允许为了出 order 而绕过 army prerequisite

### 修复后必须重跑哪一步

* `task_011_real_tactical_probe`

### 重跑仍失败时转向

* `task_010_rewrite_defend_attack_transition_logic`
* 若 army prerequisite 回归，回 `task_007`

## 9. Failure Case 7：只有 enemy combat signal，没有 friendly combat

### 现象

1. `combat_event_detected` 存在；
2. 但事件只是因为看见敌军；
3. 友军实际未接敌或无 army。

### 常见原因

1. `tactical_manager.detect_combat_event` 对 enemy visible 太敏感
2. `own_army_count = 0`
3. army 存在但未接近敌军
4. attack order / defend order 没有真正把军队带到接敌位置
5. replay 与 telemetry 不一致

### 先查哪些 artifact

1. `telemetry/events.jsonl`
2. `match.SC2Replay`

重点查：

* `combat_event_detected`
* `combat_event_skipped`
* `army_order`
* `own_army_count`
* `reason`

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`

重点字段：

* `build_order.attack_army_supply_threshold`
* `build_order.attack_game_time_threshold`
* `build_order.defend_radius`

### 再查哪些代码路径

1. `src/sc2bot/managers/tactical_manager.py`

   * combat event detection
   * plan selection
2. `src/sc2bot/runtime/game_loop.py`

### 如何区分

* `own_army_count = 0`：`missing_prerequisite`
* 有 army、有 order、但位置始终不到：`tactical_logic_failure` 或 `no_contact_under_valid_conditions`
* 只有 enemy visible 触发事件：`enemy_only_combat_signal`
* replay 缺失：`invalid_evidence`

### 修复动作

1. 把 `friendly combat` 的判定与 `enemy visible` 分开
2. 修 tactical order 到 contact 的路径
3. 若 army 根本不存在，返回 prior phase

### 修复后必须重跑哪一步

* `task_011_real_tactical_probe`

### 重跑仍失败时转向

* `task_010_rewrite_defend_attack_transition_logic`
* 或回 `task_007`

## 10. Failure Case 8：replay / result / telemetry 缺失

### 现象

1. run 看起来跑过了；
2. 但关键 artifact 缺一个或多个；
3. 报告没法支撑 claim。

### 常见原因

1. output_dir 配置错误
2. runner persistence 出错
3. run 崩溃但未 fail-fast
4. output 被旧 run 覆盖
5. paired 一侧没落盘

### 先查哪些 artifact

1. `summary.json`
2. 目录结构本身
3. `match_result.json`
4. `telemetry/events.jsonl`
5. `match.SC2Replay`

### 再查哪些配置

1. 当前 `configs/evaluation/*.yaml`
2. `output_dir`
3. `run_id`
4. `fail_on_crash`
5. `isolate_runs`

### 再查哪些代码路径

1. `evaluation/runner/run_match.py`
2. `evaluation/runner/run_batch.py`
3. `evaluation/runner/collect_results.py`

### 如何区分

* 关键 artifact 缺失：直接 `invalid_evidence`
* artifact 全在但内容冲突：仍是 `invalid_evidence`
* paired 只有一侧缺失：paired `invalid_evidence`

### 修复动作

1. 修 output_dir / run_id / isolate_runs
2. 修 persistence 合同
3. 不改 gameplay 逻辑

### 修复后必须重跑哪一步

* 原 task 同级 rerun

### 重跑仍失败时转向

* `task_002_lock_runtime_eval_contract_and_config_roles`

## 11. Failure Case 9：small eval 全是 diagnostic，不是 capability

### 现象

1. batch 跑完了；
2. 报告里全是中间信号；
3. 没有真实胜利、没有 stable gameplay evidence；
4. checkpoint 无法接受 Level 1 baseline。

### 常见原因

1. 更早 phase 的 prerequisite 根本没过
2. batch 扩大样本掩盖了前置缺口
3. run 虽多，但全是 command-only、enemy-only、diagnostic-only
4. baseline core 仍然只是 survival scaffold
5. batch 设计本身没对准当前 claim

### 先查哪些 artifact

1. `summary.json`
2. per-match `match_result.json`
3. per-match `events.jsonl`
4. `artifacts/reports/r4_baseline_easy_pool/report.md`

### 再查哪些配置

1. `configs/evaluation/r4_baseline_easy_pool_batch.yaml`
2. `configs/maps/baseline_easy_pool_maps.yaml`
3. `configs/opponents/baseline_easy_pool.yaml`
4. `configs/bot/baseline_playable.yaml`

### 再查哪些代码路径

按 dominant failure class 选：

1. build chain：`game_loop.py`
2. production：`game_loop.py`
3. tactical：`tactical_manager.py` + `game_loop.py`

### 如何区分

* evidence 缺失：`invalid_evidence`
* time 不足：`insufficient_duration`
* prerequisite 缺失：`missing_prerequisite`
* 前置能力虽有一点信号但未 validated：`diagnostic_only_batch`
* 行为不稳定：`stability_failure`

### 修复动作

1. 不要扩大 batch
2. 找 dominant failure class
3. 回对应 prior phase repair
4. 若只是轻微不稳定，再用 `task_014` 做 focused repair / confirmation

### 修复后必须重跑哪一步

* 先重跑 `task_014_baseline_repair_or_confirmation`
* 若 prior phase 失败，先回 prior phase，再重跑 `task_013`

### 重跑仍失败时转向

* 视 failure class 返回 `task_010`、`task_007` 或 `task_004`

## 12. Failure Case 10：adaptive model 只改 telemetry，不改行为

### 现象

1. `strategy_response` 或 `recommended_response_tags` 变了；
2. scout、posture、first attack timing 却没变；
3. paired report 只有 tag delta，没有 behavior delta。

### 常见原因

1. `strategy_manager.py` 只输出 tag，没有把 gate 接入 gameplay
2. `_safe_worker_scout`、tactical plan、attack timing 没读取 gate
3. control / treatment 配置其实没差
4. belief state 只做日志，不做行动偏置

### 先查哪些 artifact

1. `artifacts/reports/r5_paired_adaptive_eval/report.md`
2. control / treatment 两侧 `events.jsonl`
3. replay

重点查：

* `strategy_response`
* `adaptive_gate_applied`（若已实现）
* scout 行为差异
* defend posture 差异
* first attack timing 差异

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`
2. `configs/bot/adaptive_research.yaml`
3. `configs/evaluation/r5_paired_control.yaml`
4. `configs/evaluation/r5_paired_treatment.yaml`

重点字段：

* `opponent_model.mode`
* `opponent_model.intervention_mode`
* 与 gate 相关的新字段

### 再查哪些代码路径

1. `src/sc2bot/managers/strategy_manager.py`
2. `src/sc2bot/runtime/game_loop.py`
3. `src/sc2bot/managers/tactical_manager.py`
4. `src/sc2bot/domain/belief_state.py`（若已创建）

### 如何区分

* tag 变了、行为没变：`no_behavior_change`
* control / treatment 根本一样：`invalid_evidence` 或 config drift
* 行为似乎变了但没有 paired 对照：证据不足，不能写通过

### 修复动作

1. 把 gate 真正接到 `_safe_worker_scout`、defensive posture 或 first attack timing
2. 保持改动只限允许的三个 gate
3. 不要顺手改 build / production / unit composition

### 修复后必须重跑哪一步

* `task_017_null_vs_adaptive_paired_evaluation`

### 重跑仍失败时转向

* `task_016_integrate_single_adaptive_gating_layer`

## 13. Failure Case 11：paired A/B 没有真实差异

### 现象

1. control / treatment 跑完了；
2. paired report 看不到真实差异；
3. 可能 outcome 也没差，或只差一点随机波动。

### 常见原因

1. adaptive gate 太弱
2. treatment 没真正改变行为
3. control / treatment 不可比
4. 评测切片不触发相关 gate
5. baseline core 在 paired 期间漂移

### 先查哪些 artifact

1. control `summary.json`
2. treatment `summary.json`
3. control / treatment `events.jsonl`
4. `artifacts/reports/r5_paired_adaptive_eval/report.md`

### 再查哪些配置

1. `configs/bot/baseline_playable.yaml`
2. `configs/bot/adaptive_research.yaml`
3. `configs/evaluation/r5_paired_control.yaml`
4. `configs/evaluation/r5_paired_treatment.yaml`

### 再查哪些代码路径

1. `strategy_manager.py`
2. `game_loop.py`
3. `tactical_manager.py`
4. belief state 更新逻辑

### 如何区分

* control / treatment 不可比：`invalid_evidence`
* tag 有差异，行为无差异：`no_behavior_change`
* 行为有差异，但 outcome 无改善：`no_causal_benefit`
* paired slice 根本不触发 gate：评测设计问题，需要更换 paired slice，但不得写通过

### 修复动作

1. 先确保 paired 可比
2. 再确认至少一个 gate 会在该 slice 中被触发
3. 若 behavior 仍无差异，增强 gate 接入而不是扩大结论
4. 若 behavior 有差异但无收益，不要强行写 research success

### 修复后必须重跑哪一步

* `task_017_null_vs_adaptive_paired_evaluation`

### 重跑仍失败时转向

* 无行为差异：回 `task_016_integrate_single_adaptive_gating_layer`
* 有行为差异但无收益：维持 “research contribution not accepted”，再决定是否继续 repair
* 若 baseline 漂移：回 `checkpoint_E` 接受的 control 版本，并重新组织 paired eval

## 14. 最终规则

任何 failure 都必须回答下面五个问题之后，才能动手修：

1. 这是 evidence 问题、duration 问题、prerequisite 问题还是 logic 问题？
2. dominant failure class 是哪一个？
3. 最小必要重跑是哪一步？
4. repair 应该落在哪个 task？
5. 如果 repair 后仍失败，应该回哪个 prior phase？

如果这五个问题答不清，先不要改代码，先补分类。
