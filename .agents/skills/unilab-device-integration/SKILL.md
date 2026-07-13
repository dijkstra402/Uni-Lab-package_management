---
name: unilab-device-integration
description: 依据 device_templates_actions.csv 对 Uni-Lab 实验室设备接入进行标准化。添加、实现、审查或修改设备直连驱动、厂商协议驱动、PLC 驱动或 OPC UA 设备时使用；选择已有设备大类、定义新设备大类，或检查直连实现与 PLC 实现的动作、参数、返回类型、状态属性及类型是否一致时也使用。
---

# Uni-Lab 设备标准接入

将 `device_templates_actions.csv` 作为设备接口规范的唯一事实来源。让工作流只依赖统一接口，不依赖设备厂商、传输方式或 PLC 通信协议。

## 定位标准仓库

在同时包含 `device_templates_actions.csv` 和 `packages/` 的仓库中工作。不得使用复制后可能过期的 CSV。修改前先定位仓库根目录：

```bash
git rev-parse --show-toplevel
```

使用本技能的 `scripts/device_standard.py` 查询和校验实时 CSV。在当前目录不属于标准仓库时，通过 `--repo <仓库路径>` 明确指定仓库。

## 执行设备接入流程

1. 收集设备大类、厂商型号、物理能力、厂商协议、连接参数、命令、响应、单位、量程、超时、报警和安全约束。
2. 编写代码前先搜索现有标准：

   ```bash
   python3 .agents/skills/unilab-device-integration/scripts/device_standard.py --search '蠕动泵'
   python3 .agents/skills/unilab-device-integration/scripts/device_standard.py --device-id peristaltic_pump
   ```

3. 当现有 `device_id` 的业务语义和接口能力匹配时，直接复用。不得仅因品牌或型号不同而创建新设备大类。
4. 没有合适大类时，先提出新大类及完整动作和状态属性方案，确认设备语义清楚后再修改 CSV。
5. 分离标准接口和具体通信实现：
   - 标准模板：`packages/<device_id>/<device_id>/<device_id>.py`。
   - 直连实现：把标准动作和状态属性转换为串口、TCP、HTTP、Modbus 或厂商私有命令。
   - PLC/OPC UA 实现：把同一套接口转换为 PLC 逻辑节点的读写操作。
6. 实现设备需要的全部标准动作和状态属性。严格保持接口名称、参数名称、参数类型、默认值、返回注解和属性类型一致。
7. 交付前执行校验：

   ```bash
   python3 .agents/skills/unilab-device-integration/scripts/device_standard.py --validate --check-code <device_id>
   unilab --check_mode --devices ./packages/<device_id>/<device_id> --external_devices_only
   ```

8. 报告选用的设备大类、标准接口映射、通信协议映射、已执行的验证以及不支持的能力。没有使用真实硬件或可靠模拟器验证时，不得声称已完成硬件验证。

## 强制执行接口规则

- 让工作流代码只依赖标准动作和状态属性。
- 为具体厂商型号驱动分配唯一的 `@device` ID，并把它归入对应标准设备大类。
- 不得为了适配一个厂商而削弱整个设备大类；厂商差异应在具体驱动内部处理。
- 优先采用可向后兼容的增量修改。删除、重命名、修改参数或类型都属于破坏性变更，必须明确说明并获得用户确认。
- 动作返回结构化结果，例如 `{"success": True, "message": "..."}`。通信超时、设备拒绝、响应无效或 PLC 完成信号超时时，抛出可定位问题的错误。
- 在驱动边界校验单位和数值范围。发生单位换算时必须明确记录，不得静默转换。
- 通过属性暴露设备状态，不得用带副作用的动作读取状态。
- 保留设备或 PLC 内的安全联锁。软件驱动不得绕过防护、报警、急停或动作完成握手。

## 正确处理 PLC 和 OPC UA

- 将 PLC 接入视为底层实现方式，不得另造一套工作流接口。
- 对带参数的设置动作，写入相应设定值节点。
- 对触发动作，依次执行：写触发为 `True`、等待完成为 `True`、复位触发、等待完成恢复为 `False`。
- 轮询完成节点时强制从服务端读取，避免使用过期的订阅缓存值。
- 从对应逻辑状态节点读取状态属性。
- 在 `device_templates_actions.csv` 中保存逻辑节点名称。使用独立的现场节点映射 CSV 保存实际 OPC UA `NodeId`、`Name`、`NodeType` 和 `DataType`。不得把 `device_templates_actions.csv` 传给 `load_nodes_from_csv`，两者用途和结构不同。
- 将 `generate_plc_drivers.py` 视为批量生成器。它会重写全部 PLC 生成代码并刷新 CSV 映射列，运行后必须检查差异。
- 只有执行全仓库一致性审计时才使用 `--validate --check-code all`。单设备接入过程中发现的无关历史差异应单独报告，不得顺手批量修改。

## 按需读取详细规范

新增设备大类、修改 CSV、生成 PLC 驱动或实现具体厂商驱动前，读取 [设备接入标准](references/standard.md)。其中定义了 CSV 字段、设备大类选择规则、协议映射方式和验收清单。

