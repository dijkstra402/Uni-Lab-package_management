"""
切割机 — 标准设备类模板 (Device Class Template)

定义「切割机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="cutting_machine",
    category=["切割机"],
    description="切割机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="切割机",
)
class CuttingMachine:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "cutting_machine"
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

    @action(description="设置切割速度")
    def set_cutting_speed(self, cutting_speed: int = 0) -> Dict[str, Any]:
        """
        设置切割速度。

        Args:
            cutting_speed[设置切割速度]: 设置切割速度。
        """
        pass

    @action(description="设置切割深度")
    def set_cutting_depth(self, cutting_depth: int = 0) -> Dict[str, Any]:
        """
        设置切割深度。

        Args:
            cutting_depth[设置切割深度]: 设置切割深度。
        """
        pass

    @action(description="设置进给速率")
    def set_feed_rate(self, feed_rate: int = 0) -> Dict[str, Any]:
        """
        设置进给速率。

        Args:
            feed_rate[设置进给速率]: 设置进给速率。
        """
        pass

    @action(description="设置切割压力")
    def set_cutting_pressure(self, cutting_pressure: int = 0) -> Dict[str, Any]:
        """
        设置切割压力。

        Args:
            cutting_pressure[设置切割压力]: 设置切割压力。
        """
        pass

    @action(description="设置冷却液流量")
    def set_coolant_flow(self, coolant_flow: int = 0) -> Dict[str, Any]:
        """
        设置冷却液流量。

        Args:
            coolant_flow[设置冷却液流量]: 设置冷却液流量。
        """
        pass

    @action(description="设置刀片转速")
    def set_blade_speed(self, blade_speed: int = 0) -> Dict[str, Any]:
        """
        设置刀片转速。

        Args:
            blade_speed[设置刀片转速]: 设置刀片转速。
        """
        pass

    @action(description="设置切割精度")
    def set_cutting_precision(self, cutting_precision: int = 0) -> Dict[str, Any]:
        """
        设置切割精度。

        Args:
            cutting_precision[设置切割精度]: 设置切割精度。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
