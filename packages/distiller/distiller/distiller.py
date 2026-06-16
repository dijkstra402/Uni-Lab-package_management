"""
蒸馏器 — 标准设备类模板 (Device Class Template)

定义「蒸馏器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="distiller",
    category=["蒸馏器"],
    description="蒸馏器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="蒸馏器",
)
class Distiller:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "distiller"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置温度。

        Args:
            temperature[温度]: 目标温度（单位依设备量程而定）。
        """
        pass

    @action(description="蒸馏")
    def distill(self) -> Dict[str, Any]:
        """蒸馏。"""
        pass

    @action(description="加热")
    def heat(self) -> Dict[str, Any]:
        """加热。"""
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
    def device_ready(self) -> bool:
        """设备就绪。"""
        return self.data.get("device_ready", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def distillation_flow(self) -> float:
        """蒸馏流量。"""
        return self.data.get("distillation_flow", 0.0)
