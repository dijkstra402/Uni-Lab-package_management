"""
纯水设备 — 标准设备类模板 (Device Class Template)

定义「纯水设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="pure_water_system",
    category=["样品处理仪器与设备", "纯化设备", "纯水设备"],
    description="纯水设备标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="纯水设备",
)
class PureWaterSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "pure_water_system"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置制水流量")
    def set_water_production_flow(self, water_production_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置制水流量。

        Args:
            water_production_flow[制水流量]: 目标制水流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置水质电阻率")
    def set_water_resistivity(self, water_resistivity: float = 0.0) -> Dict[str, Any]:
        """
        设置水质电阻率。

        Args:
            water_resistivity[水质电阻率]: 目标水质电阻率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="制水")
    def produce_water(self) -> Dict[str, Any]:
        """制水。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="冲洗")
    def rinse(self) -> Dict[str, Any]:
        """冲洗。"""
        raise NotImplementedError("请在设备包中实现该动作")

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
    def current_water_resistivity(self) -> int:
        """实际水质电阻率。"""
        return self.data.get("current_water_resistivity", 0)

    @property
    @topic_config()
    def current_water_production_flow(self) -> float:
        """实际制水流量。"""
        return self.data.get("current_water_production_flow", 0.0)
