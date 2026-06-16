"""
热混匀仪 — 标准设备类模板 (Device Class Template)

定义「热混匀仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="thermomixer",
    category=["热混匀仪"],
    description="热混匀仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="热混匀仪",
)
class Thermomixer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "thermomixer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置加热温度")
    def set_heating_temperature(self, heating_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置加热温度。

        Args:
            heating_temperature[加热温度]: 目标加热温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置混匀速度")
    def set_mix_speed(self, mix_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置混匀速度。

        Args:
            mix_speed[混匀速度]: 目标混匀速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[运行时间]: 目标运行时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置工作模式")
    def set_work_mode(self, work_mode: str = "") -> Dict[str, Any]:
        """
        设置工作模式。

        Args:
            work_mode[工作模式]: 目标工作模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置温度单位")
    def set_temperature_unit(self, temperature_unit: float = 0.0) -> Dict[str, Any]:
        """
        设置温度单位。

        Args:
            temperature_unit[温度单位]: 目标温度单位（单位依设备量程而定）。
        """
        pass

    @action(description="设置加热功率")
    def set_heating_power(self, heating_power: float = 0.0) -> Dict[str, Any]:
        """
        设置加热功率。

        Args:
            heating_power[加热功率]: 目标加热功率（单位依设备量程而定）。
        """
        pass

    @action(description="设置安全温度")
    def set_safety_temperature(self, safety_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置安全温度。

        Args:
            safety_temperature[安全温度]: 目标安全温度（单位依设备量程而定）。
        """
        pass

    @action(description="混匀")
    def mix(self) -> Dict[str, Any]:
        """混匀。"""
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
    def door_switch_state(self) -> bool:
        """门开关状态。"""
        return self.data.get("door_switch_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """当前温度显示。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前速度显示。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示。"""
        return self.data.get("current_time", 0.0)
