# PLC 驱动生成与直连一致性维护 —— 规划文档

## 1. 目标

以 `packages/` 下的**直连驱动模板**（`<id>.py`）为接口基准，参照 `AI4C.py` 的真实
OPC UA 交互范式，为每个设备大类生成 **PLC 驱动**（`<id>_plc.py`），并以
`device_templates_actions.csv` 为唯一数据源统一维护。

核心约束：**PLC 驱动暴露的变量（方法名 / 参数名+类型 / 属性名）**，
使同一套工作流可在「直连」与「PLC」两种实现间无缝切换；同时在 CSV 中建立
「直连变量 ↔ PLC 节点」对照表，并提供校验脚本自动比对、报告不一致项。

## 2. 现状

| 资产                               | 说明                                                                                                                       |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `AI4C.py`                        | 真实参照例。继承`OpcUaClientWithSubscription`，节点交互范式：触发类 `_Trigger`/`_Complete`、设定类写值、状态类读节点 |
| `packages/<id>/<id>/<id>.py`     | 139 个直连模板，`@action` 方法体为 `pass`，`@property` 读 `self.data`                                              |
| `packages/<id>/<id>/<id>_plc.py` | 已由生成器产出的 PLC 驱动，方法签名与直连同源                                                                              |
| `device_templates_actions.csv`   | 2372 行，列：`设备大类, device_id, 类型, 英文名, 中文描述, 参数(名:类型), PLC节点, 交互模式`                             |
| `generate_plc_drivers.py`        | 读 CSV 生成`<id>_plc.py`，并回写 `PLC节点`/`交互模式` 两列                                                           |

**当前 PLC 节点命名规则**（`generate_plc_drivers.py`）：

- 属性 → `Pascal_Case(英文名)`，交互模式「读状态」
- 设定类动作（有参数，如 `set_speed`）→ `Pascal_Case(参数名)_Setpoint`，交互模式「写设定值」
- 触发类动作（无参数）→ `Pascal_Case(英文名)_Trigger / _Complete`，交互模式「写触发→等完成→复位」

## 3. 一致性的三层定义

1. **接口级一致（强约束）**：`<id>_plc.py` 的 action 方法名、参数名与类型、property 名集合，
   必须与 `<id>.py` 完全相同。二者均由**同一份 CSV 确定性生成**，从源头保证一致，
   不手改成品即不会漂移。
2. **节点对照（映射约束）**：CSV 中 `英文名`（直连变量）与 `PLC节点` 构成一一对照表；
   同一 `device_id` 内 `PLC节点` 唯一，命名符合第 2 节规则。
3. **CSV ↔ 代码一致（数据约束）**：CSV 每一行都在直连模板与 PLC 驱动中有对应实现，
   无多余、无缺失。

## 4. 方案

### 4.1 数据源：CSV 保持唯一真相

- 直连模板、PLC 驱动、节点对照都以 `device_templates_actions.csv` 为准。
- 不手改 `<id>_plc.py`（文件头已标注「自动生成，请勿手改」）；一致性由「同源生成」保证。
- 直连变量与 PLC 节点的对照表**内嵌在 CSV**（`英文名` 列 = 直连变量，`PLC节点` 列 = PLC 节点），
  无需额外映射文件。

### 4.2 生成器：对齐 AI4C.py（沿用现有 `generate_plc_drivers.py`）

维持现有确定性生成逻辑，交互范式与 AI4C.py 一致：

- 触发类：`set_node_value(X_Trigger, True)` → `_wait_until_true(X_Complete)` → 复位 → `_wait_until_false(X_Complete)`
- 设定类：`set_node_value(<Param>_Setpoint, 值)`
- 属性：`get_node_value(<Node>)`

生成器同时把 `PLC节点`/`交互模式` 回写 CSV，使对照表随生成自动更新。
若命名规则需微调（见第 6 节风险），仅改生成器 + 重跑，不逐个手改成品。

## 5. 执行步骤

1. 确认 CSV 中每个设备的 `英文名`/`参数(名:类型)`/`类型` 准确，作为直连与 PLC 的共同接口定义。
2. 运行 `generate_plc_drivers.py`：生成 `<id>_plc.py`，并回写 `PLC节点`/`交互模式`。
3. 抽查若干设备，确认 PLC 方法签名与直连模板一致、CSV 对照表节点无冲突。
4. 若发现命名冲突或规则偏差，改 CSV（数据）或生成器（规则）后重跑第 2 步。

## 6. 风险与注意

- **节点名冲突**：不同直连变量经 `pascal()` 可能映射到同名节点（大小写/分词差异）。
  抽查时留意；如遇冲突，在生成器加消歧规则并重跑。
- **AI4C.py 的复杂交互不可完全模板化**：真实设备有占位检查、多参数、枚举编码、位置索引
  （如 `Robotic_Arm_Target_Position_Code`）等。模板化生成只覆盖「触发/设定/读状态」三种标准范式；
  超出部分标注为需人工对接，不强行生成。
- **直连模板是 `pass` 占位**：一致性针对的是**接口签名**，不涉及方法体行为。
- **不改动 `AI4C.py`**：它是参照真值，只读不写。

## 7. 交付物

- `PLC_GENERATION_PLAN.md`（本文档）
- 重新生成的 `<id>_plc.py`（139 个设备）
- 更新后的 `device_templates_actions.csv`（含 `PLC节点`/`交互模式` 对照列）
