"""
蒸馏水设备 — 标准设备类模板 (Device Class Template)

定义「蒸馏水设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="distilled_water_system",
    category=["蒸馏水设备"],
    description="蒸馏水设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="蒸馏水设备",
)
class DistilledWaterSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "distilled_water_system"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: int = 0) -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[设置运行模式]: 设置运行模式。
        """
        pass

    @action(description="蒸馏")
    def distill(self, distillation_flow: int = 0) -> Dict[str, Any]:
        """
        蒸馏。

        Args:
            distillation_flow[蒸馏流量设置]: 蒸馏流量设置。
        """
        pass

    @action(description="加热")
    def heat(self, heating_temperature: int = 0) -> Dict[str, Any]:
        """
        加热。

        Args:
            heating_temperature[加热温度设置]: 加热温度设置。
        """
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_heating_temperature(self) -> int:
        """实际加热温度。"""
        return self.data.get("current_heating_temperature", 0)

    @property
    @topic_config()
    def current_distillation_flow(self) -> int:
        """实际蒸馏流量。"""
        return self.data.get("current_distillation_flow", 0)
