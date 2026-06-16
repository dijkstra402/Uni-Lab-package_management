"""
真空泵 — 标准设备类模板 (Device Class Template)

定义「真空泵」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vacuum_pump",
    category=["真空泵"],
    description="真空泵标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="真空泵",
)
class VacuumPump:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "vacuum_pump"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置目标真空度")
    def set_target_vacuum(self, target_vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置目标真空度。

        Args:
            target_vacuum[目标真空度]: 目标目标真空度（单位依设备量程而定）。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
        pass

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        pass

    @property
    @topic_config()
    def status(self) -> str:
        """设备运行状态。"""
        return self.data.get("status", "idle")

    @property
    @topic_config()
    def fault(self) -> bool:
        """故障。"""
        return self.data.get("fault", False)

    @property
    @topic_config()
    def idle(self) -> bool:
        """空闲。"""
        return self.data.get("idle", False)

    @property
    @topic_config()
    def high_pressure_protection_state(self) -> bool:
        """高压保护状态。"""
        return self.data.get("high_pressure_protection_state", False)

    @property
    @topic_config()
    def low_pressure_protection_state(self) -> bool:
        """低压保护状态。"""
        return self.data.get("low_pressure_protection_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """当前真空度显示。"""
        return self.data.get("current_vacuum", 0.0)
