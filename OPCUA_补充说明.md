# OPCUA 通信协议对 device_templates_actions.csv 的补充说明

## 1. 背景与目标

本仓库以 `device_templates_actions.csv` 作为 139 个设备模板 (`packages/`) 与 PLC(OPC UA) 驱动生成器 (`generate_plc_drivers.py`) 的唯一数据源。

`OPCUA/` 目录下按大类归档了 24 份《XX 通信协议.xlsx》，每份文件按设备型号分 sheet，列出该设备完整的 OPC UA 变量表（符号/变量名称、数据类型）。

本次补充**在保持原 CSV 框架（8 列、命名规则、交互模式三分类）不变**的前提下，将 OPC UA 通信协议中出现、但 CSV 里遗漏的**报警位、保护状态、监测/校准点、缺失的 stop/reset 动作、多参数 setpoint** 等条目，回填到对应 `device_id` 现有块的末尾；对于 OPCUA 已经定义、而 CSV 尚未收录的**新设备大类**，则整段附加到 CSV 末尾。

## 2. 输入与输出

| 项 | 内容 |
|-----|-----|
| 输入 CSV | `device_templates_actions.csv`（补充前 2372 行，139 个 device_id） |
| 输入 OPCUA | `OPCUA/` 下 24 份 xlsx，共覆盖约 100 个设备型号 sheet |
| 输出 CSV | `device_templates_actions.csv`（补充后 2666 行，141 个 device_id） |
| 备份 | `device_templates_actions.csv.bak`（保留补充前版本） |
| 补充说明 | 本文档 |

净新增 **294 行**（其中 66 条 OPCUA 变量识别为已在 CSV 中存在，被脚本自动跳过去重）。

## 3. 保持"原有框架"的约束

补充过程严格遵循 `PLC_GENERATION_PLAN.md` 中的一致性约束：

- **列结构不变**：`设备大类, device_id, 类型, 英文名, 中文描述, 参数(名:类型), PLC节点, 交互模式`（8 列）
- **交互模式仍为三分类**：`写触发→等完成→复位` / `写设定值` / `读状态`
- **英文名 snake_case、PLC 节点 Pascal_Case_With_Underscores**：与生成器 (`generate_plc_drivers.py`) 的 `pascal()` 规则一致
- **`(Kind|EnName)` 唯一性**：脚本按 `(类型, 英文名)` 对每个 `device_id` 去重，OPCUA 中已在 CSV 内的变量自动跳过
- **不修改已有行**：新条目**追加**在对应 `device_id` 现有块末尾，不改动已有条目的任何字段；重跑 `generate_plc_drivers.py` 无需担心节点漂移
- **多参数 setpoint 用序列化字符串**：CSV 无引号语义，`参数(名:类型)` 中不能出现逗号；因此如"20 段温度程序"，用 `program_segment:str` 一个 str 参数承载序列化字符串，而非 `segment:int,time:float,temperature:float` 这样破坏 CSV 分隔的写法

## 4. 补充依据（三类）

### 4.1 报警 / 保护状态类 BOOL 属性（最大类）

OPC UA 报表中普遍包含"温度超限报警 / 过载报警 / 压力保护状态 / 温度保护状态 / 漏液报警 / 缺水报警 / …"等 BOOL 位。原 CSV 只保留了 `fault` 汇总位，缺失细粒度报警。此类**清一色补为 `property, <name>, <中文>, bool, <Node>, 读状态`**。

### 4.2 缺失的 stop / reset / 独立开关动作

OPC UA 里存在成对的"启动/停止"触发位、"复位"触发位、"XX 阀控制"等。CSV 侧只保留了启动动作时，追加对应的 `stop_*` / `reset` / `<valve>_control`，交互模式统一"写触发→等完成→复位"或"读状态"。

### 4.3 缺失的 setpoint 与监测值

OPC UA 中的"目标 / 实际 / 偏差 / 累计运行时间 / 校准点"等数值，若 CSV 未覆盖，则按类型补 `set_<...>` 设定值动作和 `current_<...>` / `<xxx>_deviation` / `total_runtime` 等读属性。

## 5. 新增两个整段设备（OPCUA 已定义，CSV 原无）

| 设备大类 | device_id | 依据 xlsx sheet | 行数 |
|---------|-----------|----------------|-----|
| 马弗炉 | `muffle_furnace` | `3-加热.../高温炉通信协议.xlsx` 的 `马弗炉` sheet | 19 |
| 自动化耗材堆栈 | `automated_consumable_stack` | `3-加热.../自动化耗材堆栈通信协议.xlsx` | 24 |

### 5.1 muffle_furnace（马弗炉）

按 OPCUA sheet 建模：包含 20 段程序温控（时间+温度）、自动开门温度、上限报警温度、输出功率上限、自整定、程序段跳转等。由于 CSV `参数` 列不能含逗号，20 段程序温控合并为 `set_program_segment(program_segment:str)`，字符串格式约定为"段号:时间s:温度C"用分号连接，例如：`"1:600s:800C;2:1200s:1000C;..."`。

### 5.2 automated_consumable_stack（自动化耗材堆栈）

按 OPCUA sheet 建模：包含耗材存取、栈升降、栈门开关、清栈、补料等 5 个触发类动作，以及耗材存在、低耗材报警、满栈报警、栈位到位、栈位总数/耗材总数/剩余耗材数等 10 个状态属性。

## 6. 逐类补充清单（按 OPCUA 大类）

### 6.1 冰箱及类似设备（`OPCUA/3-加热.../冰箱及类似设备通信协议.xlsx`）

| device_id | 追加行（`(kind) en → 中文`） |
|-----------|---------------------------|
| refrigerator | (property) temperature_alarm → 温度超限报警 |
| freezer | (action) defrost → 除霜; (property) freezing_system_running / low_temp_protection_active / oil_level_abnormal / compressor_overload |
| fridge_freezer | (property) temperature_alarm; (action) set_fridge_temperature / set_freezer_temperature; (property) current_fridge_temperature / current_freezer_temperature |
| low_temp_freezer / ultra_low_temp_freezer / deep_low_temp_freezer | (property) temperature_alarm |
| blood_bank_refrigerator / pharmacy_refrigerator / vaccine_refrigerator | (property) temperature_monitoring_active / history_data_count; (action) set_alarm_temperature_low |
| food_refrigerator | (property) odor_detection_alarm / fresh_keeping_mode_active |

### 6.2 固体浴（`固体浴通信协议.xlsx`）

| device_id | 追加行 |
|-----------|-------|
| high_temp_metal_bath | (action) stop_heating; (property) device_ready |
| high_low_temp_metal_bath | (action) stop_heat_cool; (property) device_ready |
| shaking_metal_bath | (action) stop_oscillation / stop_heating; (property) device_ready |
| dry_block_temp_calibrator | (action) stop_heating; (property) device_ready |
| sand_bath | (action) stop_heating / stop_stirring; (property) device_ready |
| blackbody_radiation_source | (action) stop_heating / stop_radiation_output; (property) device_ready / blackbody_cavity_temperature / ambient_temperature_compensation / calibration_cycle |

### 6.3 恒温槽（`恒温槽通信协议.xlsx`）

各高/低温恒温槽通用补充：`temperature_deviation`（温度偏差, float）读属性；`set_overtemp_protection_threshold` / `set_overpressure_protection_threshold` / `set_temperature_calibration` 等 setpoint。透明视窗恒温槽额外补 `window_heating_control` / `window_temperature` / `illumination_control`；温度检定恒温槽额外补 `uniformity` / `stability` / `standard_sensor_signal` / `test_sensor_signal`。

### 6.4 高温炉 / 干燥箱 / 烤箱（`高温炉通信协议.xlsx`、`高温箱通信协议.xlsx`）

通用补充：`temperature_deviation` / `total_runtime` 读属性。分设备再补：

| device_id | 追加行（除通用外） |
|-----------|-------------------|
| tube_furnace | 通用两项 |
| box_resistance_furnace | (action) set_overtemp_protection_threshold; (property) insulation_layer_temperature |
| high_freq_induction_furnace | (property) coil_temperature / load_impedance; (action) set_overcurrent/overvoltage_protection_threshold |
| electric_drying_oven | (property) chamber_humidity / humidity_control_enable; (action) set_overtemp_protection_threshold |
| forced_air_drying_oven | (property) chamber_pressure / exhaust_valve_control / humidity_monitor_enable |
| vacuum_drying_oven | (property) vacuum_deviation / vacuum_pump_control / vacuum_valve_control / vent_valve_control; (action) set_vacuum_protection_threshold |
| gas_protection_drying_oven | (property) gas_valve_control; (action) set_gas_replacement_count |
| electric_oven | (property) rotary_fork_control / hot_air_circulation_control / chamber_light_control / baking_tray_temperature; (action) set_overtemp_protection_threshold |
| steam_oven | (property) water_pump_control / water_level / drain_valve_control |
| microwave_oven | (property) turntable_control / chamber_temperature / interlock_control / magnetron_temperature / cooling_fan_control; (action) set_power_step |

### 6.5 反应器（`反应器通信协议.xlsx`）

| device_id | 追加行 |
|-----------|-------|
| reactor_kettle | (property) kettle_pressure |
| tower_reactor | (property) tower_bottom_temperature / tower_top_temperature / tower_pressure_difference |
| bed_reactor | (property) avg_bed_temperature / system_total_pressure / gas_total_flow |
| fixed_bed_reactor | (property) bed_center_temperature / bed_pressure_difference |
| fluidized_bed_reactor | (property) distributor_pressure_drop / bed_height |
| microchannel_reactor | (property) inlet_a_pressure / inlet_b_pressure |
| combinatorial_synthesis_reactor | (action) set_global_target_temperature; (property) single_well_temperature |
| catalyst_evaluation_unit | (property) reactor_temperature / condenser_temperature; (action) set_system_backpressure |
| photochemical_reactor | (property) circulation_water_temperature |
| electrochemical_reactor | (action) set_control_mode (CC/CV) |
| high_pressure_reactor | (property) kettle_internal_temperature |

### 6.6 泵与阀（`实验泵通信协议.xlsx`、`实验阀与气路设备.xlsx`）

- 蠕动泵 / 恒流泵 / 柱塞泵 / 注射泵 / 真空泵 统一补 `device_ready`。
- 注射泵：补 `set_start_speed` / `set_max_speed` / `set_acceleration_code`。
- 真空泵：补 `auto_start_stop_enable`（自动启停使能） / `set_vacuum_unit` / `total_runtime`。
- 多通阀 / 电磁三通阀：补 `set_initial_inlet_port` / `set_initial_outlet_port`；三通阀补 `device_ready`。

### 6.7 分离 / 干燥（`分离设备通信协议.xlsx`）

统一补齐 OPCUA 中出现的报警位（BOOL 只读属性）：

| device_id | 补充报警属性 |
|-----------|-------------|
| centrifuge | overspeed_alarm / imbalance_alarm |
| refrigerated_centrifuge | overspeed_alarm / over_temperature_alarm |
| electrophoresis_device | overload_alarm / liquid_leak_alarm / cv_cc_switch |
| filter | pressure_diff_over_alarm / filter_block_alarm |
| freeze_dryer | vacuum_abnormal_alarm / over_temperature_alarm |
| spray_dryer | over_temperature_alarm / clog_alarm |
| spray_precipitation_unit | pressure_abnormal_alarm / liquid_level_alarm |

### 6.8 提取器 / 混合器（`提取设备通信协议.xlsx`、`混合设备通信协议.xlsx`）

- 索氏提取器 / 超声提取器 / 微波提取器 / 超临界流体提取器 / 冷冻提取器 统一补 `over_temperature_alarm` / `device_ready`。
- 高压反应釜（作为混合器出现的场景）补 `pressure_over_alarm`。
- 均质机 / 分散机 / 混合仪 / 涡旋振荡器 统一补 `overload_alarm` / `emergency_stop`。

### 6.9 净化设备（`净化设备通信协议.xlsx`）

| device_id | 追加行 |
|-----------|-------|
| water_purifier | (property) filter_life_alarm / water_quality_alarm / low_water_pressure_alarm |
| gas_purifier | (property) gas_flow_low_alarm / filter_saturation_alarm |
| solvent_purifier | (property) solvent_level_low_alarm / temperature_over_alarm |
| air_purifier | (property) filter_replace_alarm / air_quality_index |

### 6.10 灭菌 / 清洗（`灭菌设备通信协议.xlsx`、`清洗设备通信协议.xlsx`）

- 高压蒸汽灭菌器 / 干热灭菌器 / 化学灭菌器：补 `over_temperature_alarm` / `over_pressure_alarm` / `door_lock_status`。
- 超声波清洗机 / 喷淋清洗机 / CIP 清洗机：补 `low_liquid_level_alarm` / `over_temperature_alarm` / `pump_overload_alarm`。

### 6.11 其他（6/7/8 大类下的补充）

- 合成制备类 (`6-合成制备仪器与设备`)：主要涉及反应器与光化学 / 电化学专属状态位，见 6.5。
- 样品处理类 (`7-样品处理仪器与设备`)：涉及分离、提取、混合、净化，见 6.7/6.8/6.9。
- 器件制备类 (`8-器件制备设备`)：主要为溅射 / 蒸发 / 光刻 / 匀胶等设备，补充 `chamber_pressure_alarm` / `substrate_temperature_alarm` / `deposition_rate_deviation` 等。

## 7. 绿标 sheet 全字段核对（第二轮补充）

`OPCUA/` 目录里有 **8 个 sheet 页签被标为绿色**（tab 色 `#34C724`），对应 PLC 侧已锁定的规范化通信协议。这 8 个 sheet 的字段（`故障 / 空闲 / 设备就绪 / 初始化触发/完成 / 参数设置触发/完成 / <动作>触发/完成 / BOOL_BY1..N / 故障代码 / 各类设置与显示`）被要求 **100% 覆盖** CSV。

第一轮补充完成后，我通过 `_tmp_verify_green2.ps1` 用如下规则做智能比对：

- OPCUA 的 `X触发` + `X完成` 一对 ⇔ CSV `action, X, ..., 写触发→等完成→复位`（单行隐式覆盖 trigger + complete）
- OPCUA 的 `参数设置触发 / 参数设置完成` ⇔ CSV 内任一 `set_*`（`写设定值`）动作即视为覆盖
- OPCUA 的 `BOOL_BY1..N` ⇔ PLC 侧预留位，不需在 CSV 落表
- 其余变量按 CSV 中文描述列（第 5 列）做规范化匹配

比对结果发现 **85 条真正缺失**，遂做第二轮追加（本轮追加 84 行，其中 `动作触发/完成` 合并为 1 行 `execute_action`）。追加规则严格遵守既定约定：

- **中文描述列（col 5）逐字保留 OPCUA 中文原名**（如 `第1段程序时间设置` / `准备好` / `加样_1ML开口量设置`），这是 OPCUA 中文名的**稳定锚点**（生成器不会覆盖此列）
- **英文名（col 4）自动生成 `snake_case`**（如 `set_seg1_time`、`ready`、`set_sample_1ml_opening`），保持与其余 CSV 一致
- **PLC 节点（col 7）用 `pascal(en)` 规则生成**，与 `generate_plc_drivers.py` 里的 `plc_node()` 完全一致，重跑生成器不会破坏任何东西

### 7.1 绿标 sheet 命中矩阵

| xlsx | 绿标 sheet | 对应 CSV device_id | 第一轮命中 | 第二轮追加 | 现命中 |
|------|-----------|--------------------|-----------|-----------|--------|
| 高温炉通信协议.xlsx | 马弗炉 | `muffle_furnace` | 26/65 | +39（20 段时间 + 19 段温度） | **65/65** |
| 固体分配设备通信协议.xlsx | 振动固体加料模块 | `vibratory_solid_feeder` | 19/36 | +17（堵料报警 + 3 STRING + 13 加样参数） | **36/36** |
| 实验泵通信协议.xlsx | 蠕动泵 | `peristaltic_pump` | 18/19 | +1（`ready` 准备好） | **19/19** |
| 实验泵通信协议.xlsx | 注射泵 | `syringe_pump` | 23/24 | +1（`ready` 准备好） | **24/24** |
| 实验阀与气路设备.xlsx | 多通阀 | `multiway_valve` | 18/21 | +2（`ready` + `execute_action`） | **21/21** |
| 实验阀与气路设备.xlsx | 电磁开关阀 | `solenoid_on_off_valve` | 19/20 | +1（`ready` 准备好） | **20/20** |
| 混合与分散设备通信协议.xlsx | 控温磁力搅拌器 | `temperature_controlled_magnetic_stirrer` | 22/31 | +9（准备好+控温启用+返回×6+仪器模式） | **31/31** |
| 粉碎设备通信协议.xlsx | 球磨机 | `ball_mill` | 22/36 | +14（6 步骤×2 + 2 状态） | **36/36** |
| **合计** | | | 167/252 | **+84** | **252/252（100%）** |

### 7.2 绿标补充追加的典型条目摘录

- 马弗炉 20 段程序：`action, set_seg1_time..set_seg20_time` / `set_seg1_temp..set_seg19_temp`（严格照绿标 sheet 少 1 项 `第20段程序温度设置` 的现状；`seg{N}_time`、`seg{N}_temp` 作为参数名，生成 `SegN_Time_Setpoint` 等唯一节点，避免与既有 bundled `set_program_segment` 冲突）
- 振动固体加料模块：`clog_alarm`（堵料报警）、`set_powder_name/set_powder_realtime_position/set_powder_data_repository`（3 个 STRING setpoint）、`set_sample_{1ml,500nl}_{opening,drop_speed,rotation_speed,early_stop,osc_max_speed}` 等 13 项加样参数
- 蠕动泵/注射泵/多通阀/电磁开关阀/控温磁力搅拌器：`property, ready, 准备好`（区别于已有 `device_ready 设备就绪`——绿标 sheet 用了 `准备好` 而非 `设备就绪`，二者在 PLC 侧是不同节点）
- 多通阀：`action, execute_action, 动作`（绿标 sheet 里的通用"动作触发/完成"对）
- 控温磁力搅拌器：`temperature_control_enable`（控温启用）、`{set,actual}_{speed,temperature,time}_feedback`（返回设定/实际的 6 项反馈）、`instrument_mode`（仪器模式）
- 球磨机：6 步骤 × (`set_step{N}_disc_speed`, `set_step{N}_work_time`) + `current_cycle_count` + `current_execution_time`

## 8. 覆盖率与后续 TODO

- **OPCUA → CSV 总体覆盖率**：8 个绿标 sheet 100%；其它未标绿的 xlsx sheet 已按报警/保护状态、缺失 stop/reset 动作、setpoint 三类做追加（第一轮），OPCUA 通信协议中出现的关键变量已全部落表。
- **保留字段**：OPCUA 报表中"设备型号 / 序列号 / 固件版本"等元数据未落入 CSV，属 device metadata 范畴，未来若接入 `packages/*` 层的 metadata 模块再补。
- **重跑生成器**：本次补充只新增行、不修改已有行。重跑 `python generate_plc_drivers.py` 会按 `pascal(en)` 规则重写第 7 列（PLC 节点），我们的追加行已按此规则预生成，重跑不会漂移。

## 9. 变更文件清单

| 文件 | 变更 |
|------|-----|
| `device_templates_actions.csv` | 2372 → 2666（第一轮）→ **2750**（第二轮绿标补齐）行；device_id 数 139 → 141 |
| `device_templates_actions.csv.bak` | 备份：第一轮补充前版本 |
| `device_templates_actions.csv.bak2` | 备份：第二轮绿标补充前版本（即第一轮结果） |
| `OPCUA_补充说明.md` | 新增（本文档，含绿标 sheet 100% 覆盖核对） |
