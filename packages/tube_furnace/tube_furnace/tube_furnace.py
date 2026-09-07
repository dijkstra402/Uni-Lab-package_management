"""
管式炉 — 标准设备类模板 (Device Class Template)

定义「管式炉」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="tube_furnace",
    category=["加热、制冷及空气净化与调节设备", "恒温箱及类似设备", "高温炉", "管式炉"],
    description="管式炉标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="管式炉",
)
class TubeFurnace:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "tube_furnace"
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

    @action(description="设置升温速率")
    def set_ramp_rate(self, ramp_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置升温速率。

        Args:
            ramp_rate[升温速率]: 目标升温速率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置降温速率")
    def set_cooldown_rate(self, cooldown_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置降温速率。

        Args:
            cooldown_rate[降温速率]: 目标降温速率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置恒温时间")
    def set_hold_time(self, hold_time: float = 0.0) -> Dict[str, Any]:
        """
        设置恒温时间。

        Args:
            hold_time[恒温时间]: 目标恒温时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """
        设置加热功率。

        Args:
            heating_power[加热功率]: 目标加热功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置炉管转速")
    def set_furnace_tube_speed(self, furnace_tube_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置炉管转速。

        Args:
            furnace_tube_speed[炉管转速]: 目标炉管转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置气体流量")
    def set_gas_flow(self, gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置气体流量。

        Args:
            gas_flow[气体流量]: 目标气体流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置温度")
    def set_temperature(self, temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置温度。

        Args:
            temperature[温度]: 目标温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
    def current_run_step(self) -> int:
        """当前运行步骤。"""
        return self.data.get("current_run_step", 0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """当前温度。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def remaining_hold_time(self) -> float:
        """剩余恒温时间。"""
        return self.data.get("remaining_hold_time", 0.0)

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """实际加热功率。"""
        return self.data.get("current_heating_power", 0.0)

    @property
    @topic_config()
    def current_furnace_tube_speed(self) -> float:
        """实际炉管转速。"""
        return self.data.get("current_furnace_tube_speed", 0.0)

    @property
    @topic_config()
    def current_vacuum(self) -> float:
        """实际真空度。"""
        return self.data.get("current_vacuum", 0.0)

    @property
    @topic_config()
    def current_gas_flow(self) -> float:
        """实际气体流量。"""
        return self.data.get("current_gas_flow", 0.0)
