"""
控温磁力搅拌器 — 标准设备类模板 (Device Class Template)

定义「控温磁力搅拌器」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="temperature_controlled_magnetic_stirrer",
    category=["控温磁力搅拌器"],
    description="控温磁力搅拌器标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="控温磁力搅拌器",
)
class TemperatureControlledMagneticStirrer:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "temperature_controlled_magnetic_stirrer"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌速度。

        Args:
            stir_speed[搅拌速度]: 目标搅拌速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置加热温度")
    def set_heating_temperature(self, heating_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置加热温度。

        Args:
            heating_temperature[加热温度]: 目标加热温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置时间")
    def set_time(self, time: float = 0.0) -> Dict[str, Any]:
        """
        设置时间。

        Args:
            time[时间]: 目标时间（单位依设备量程而定）。
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

    @action(description="设置加热模式")
    def set_heating_mode(self, heating_mode: str = "") -> Dict[str, Any]:
        """
        设置加热模式。

        Args:
            heating_mode[加热模式]: 目标加热模式（具体取值由设备型号定义）。
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

    @action(description="设置安全温度")
    def set_safety_temperature(self, safety_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置安全温度。

        Args:
            safety_temperature[安全温度]: 目标安全温度（单位依设备量程而定）。
        """
        pass

    @action(description="搅拌")
    def stir(self) -> Dict[str, Any]:
        """搅拌。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前速度显示。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """当前温度显示。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示。"""
        return self.data.get("current_time", 0.0)
