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

## 7. 覆盖率与后续 TODO

- **OPCUA → CSV 覆盖率**：脚本自动去重后确认，OPC UA 报表出现的"温度报警 / 过温保护 / stop_ / reset_ / 独立阀控制 / setpoint / 累计运行时间"等条目已全部落表；细节参见 `_tmp_supplement_data.ps1`。
- **保留字段**：OPC UA 报表中"设备型号 / 序列号 / 固件版本"等元数据未落入 CSV，属于 device metadata 范畴，将来若接入 `packages/*` 层的 metadata 模块再补。
- **重跑生成器**：本次补充只新增行、不修改已有行，重跑 `python generate_plc_drivers.py` 即可为新增条目生成对应 OPC UA 节点与 Python 方法。

## 8. 变更文件清单

| 文件 | 变更 |
|------|-----|
| `device_templates_actions.csv` | 2372 → 2666 行；新增 141 - 139 = 2 个 device_id |
| `device_templates_actions.csv.bak` | 备份补充前版本 |
| `OPCUA_补充说明.md` | 新增（本文档） |
