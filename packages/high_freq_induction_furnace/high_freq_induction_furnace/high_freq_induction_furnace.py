"""
高频感应炉 — 标准设备类模板 (Device Class Template)

定义「高频感应炉」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="high_freq_induction_furnace",
    category=["加热、制冷及空气净化与调节设备", "恒温箱及类似设备", "高温炉", "高频感应炉"],
    description="高频感应炉标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="高频感应炉",
)
class HighFreqInductionFurnace:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "high_freq_induction_furnace"
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

    @action(description="设置感应功率")
    def set_induction_power(self, induction_power: float = 0.0) -> Dict[str, Any]:
        """
        设置感应功率。

        Args:
            induction_power[感应功率]: 目标感应功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置振荡频率")
    def set_oscillation_frequency(self, oscillation_frequency: float = 0.0) -> Dict[str, Any]:
        """
        设置振荡频率。

        Args:
            oscillation_frequency[振荡频率]: 目标振荡频率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置加热时间")
    def set_heating_time(self, heating_time: float = 0.0) -> Dict[str, Any]:
        """
        设置加热时间。

        Args:
            heating_time[加热时间]: 目标加热时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置冷却水流速")
    def set_cooling_water_velocity(self, cooling_water_velocity: float = 0.0) -> Dict[str, Any]:
        """
        设置冷却水流速。

        Args:
            cooling_water_velocity[冷却水流速]: 目标冷却水流速（单位依设备量程而定）。
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
    def current_induction_power(self) -> float:
        """实际感应功率。"""
        return self.data.get("current_induction_power", 0.0)

    @property
    @topic_config()
    def current_oscillation_frequency(self) -> float:
        """实际振荡频率。"""
        return self.data.get("current_oscillation_frequency", 0.0)

    @property
    @topic_config()
    def remaining_heating_time(self) -> float:
        """剩余加热时间。"""
        return self.data.get("remaining_heating_time", 0.0)

    @property
    @topic_config()
    def current_cooling_water_velocity(self) -> float:
        """实际冷却水流速。"""
        return self.data.get("current_cooling_water_velocity", 0.0)
