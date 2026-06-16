"""
温度检定恒温槽 — 标准设备类模板 (Device Class Template)

定义「温度检定恒温槽」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="temp_verification_thermostatic_bath",
    category=["温度检定恒温槽"],
    description="温度检定恒温槽标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="温度检定恒温槽",
)
class TempVerificationThermostaticBath:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "temp_verification_thermostatic_bath"
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

    @action(description="设置控温精度")
    def set_temp_control_precision(self, temp_control_precision: int = 0) -> Dict[str, Any]:
        """
        设置控温精度。

        Args:
            temp_control_precision[控温精度]: 目标控温精度（单位依设备量程而定）。
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

    @action(description="设置制冷功率")
    def set_cooling_power(self, cooling_power: float = 0.0) -> Dict[str, Any]:
        """
        设置制冷功率。

        Args:
            cooling_power[制冷功率]: 目标制冷功率（单位依设备量程而定）。
        """
        pass

    @action(description="设置循环泵转速")
    def set_circulation_pump_speed(self, circulation_pump_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置循环泵转速。

        Args:
            circulation_pump_speed[循环泵转速]: 目标循环泵转速（单位依设备量程而定）。
        """
        pass

    @action(description="设置检定时间")
    def set_verification_time(self, verification_time: float = 0.0) -> Dict[str, Any]:
        """
        设置检定时间。

        Args:
            verification_time[检定时间]: 目标检定时间（单位依设备量程而定）。
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
    def target_temperature(self) -> float:
        """目标温度。"""
        return self.data.get("target_temperature", 0.0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """当前温度。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_heating_power(self) -> float:
        """实际加热功率。"""
        return self.data.get("current_heating_power", 0.0)

    @property
    @topic_config()
    def current_cooling_power(self) -> float:
        """实际制冷功率。"""
        return self.data.get("current_cooling_power", 0.0)

    @property
    @topic_config()
    def current_circulation_pump_speed(self) -> float:
        """实际循环泵转速。"""
        return self.data.get("current_circulation_pump_speed", 0.0)

    @property
    @topic_config()
    def liquid_level(self) -> float:
        """液位监测。"""
        return self.data.get("liquid_level", 0.0)

    @property
    @topic_config()
    def pressure(self) -> float:
        """压力监测。"""
        return self.data.get("pressure", 0.0)

    @property
    @topic_config()
    def remaining_verification_time(self) -> float:
        """剩余检定时间。"""
        return self.data.get("remaining_verification_time", 0.0)
