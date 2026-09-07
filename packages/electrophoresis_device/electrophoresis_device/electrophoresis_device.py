"""
电泳仪 — 标准设备类模板 (Device Class Template)

定义「电泳仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="electrophoresis_device",
    category=["样品处理仪器与设备", "分离设备", "电泳仪"],
    description="电泳仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="电泳仪",
)
class ElectrophoresisDevice:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "electrophoresis_device"
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

    @action(description="设置电压")
    def set_voltage(self, voltage: float = 0.0) -> Dict[str, Any]:
        """
        设置电压。

        Args:
            voltage[电压]: 目标电压（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置电流")
    def set_current(self, current: float = 0.0) -> Dict[str, Any]:
        """
        设置电流。

        Args:
            current[电流]: 目标电流（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置功率")
    def set_power(self, power: float = 0.0) -> Dict[str, Any]:
        """
        设置功率。

        Args:
            power[功率]: 目标功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="电泳")
    def electrophoresis(self) -> Dict[str, Any]:
        """电泳。"""
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
    def current_voltage(self) -> float:
        """实际电压。"""
        return self.data.get("current_voltage", 0.0)

    @property
    @topic_config()
    def current_current(self) -> float:
        """实际电流。"""
        return self.data.get("current_current", 0.0)
