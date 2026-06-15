"""
均质器 — 标准设备类模板 (Device Class Template)

定义「均质器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="homogenizer",
    category=["均质器"],
    description="均质器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="均质器",
)
class Homogenizer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "homogenizer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行时间")
    def set_run_time(self, run_time: int = 0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[设置运行时间]: 设置运行时间。
        """
        pass

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """
        设置循环次数。

        Args:
            cycle_count[设置循环次数]: 设置循环次数。
        """
        pass

    @action(description="设置压力上限")
    def set_pressure_upper_limit(self, pressure_upper_limit: int = 0) -> Dict[str, Any]:
        """
        设置压力上限。

        Args:
            pressure_upper_limit[设置压力上限]: 设置压力上限。
        """
        pass

    @action(description="设置流量上限")
    def set_flow_upper_limit(self, flow_upper_limit: int = 0) -> Dict[str, Any]:
        """
        设置流量上限。

        Args:
            flow_upper_limit[设置流量上限]: 设置流量上限。
        """
        pass

    @action(description="均质")
    def homogenize(self, homogenize_pressure: int = 0, homogenize_flow: int = 0, homogenize_level: int = 0) -> Dict[str, Any]:
        """
        均质。

        Args:
            homogenize_pressure[均质压力设置]: 均质压力设置。
            homogenize_flow[均质流量设置]: 均质流量设置。
            homogenize_level[均质级别设置]: 均质级别设置。
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
    def current_pressure(self) -> int:
        """当前压力显示。"""
        return self.data.get("current_pressure", 0)

    @property
    @topic_config()
    def current_flow(self) -> int:
        """当前流量显示。"""
        return self.data.get("current_flow", 0)

    @property
    @topic_config()
    def current_time(self) -> int:
        """当前时间显示。"""
        return self.data.get("current_time", 0)

    @property
    @topic_config()
    def current_cycle_count(self) -> int:
        """当前循环次数。"""
        return self.data.get("current_cycle_count", 0)

    @property
    @topic_config()
    def temperature(self) -> int:
        """温度监测显示。"""
        return self.data.get("temperature", 0)
