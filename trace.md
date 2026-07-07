# Trace: Uni-Lab-package_management

<!-- concepts: PLC/OPC-UA 设备驱动, 代码生成, 设备模板标准化 -->

## 2026-07-06 生成 139 个 PLC 交互驱动

- 任务：把 packages/ 下 139 个设备模板类（`@action` 空实现 + `@property`）改写为 AI4C.py 那样的 PLC(OPC UA) 交互驱动。
- 方案：写 `generate_plc_drivers.py`，以 `device_templates_actions.csv` 为唯一数据源，确定性生成 `<id>_plc.py`（同级新建，保留原模板）。
- 交互范式：触发类动作=写 `<X>_Trigger` 等 `<X>_Complete` 复位；设定类 `set_*`=写 `<Param>_Setpoint`；属性=读节点。
- CSV 追加两列：`PLC节点`、`交互模式`。
- 决策来自用户 AskUserQuestion：`_plc.py` 同级新建、生成器+成品、节点+交互模式列。
