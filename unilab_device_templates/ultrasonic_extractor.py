"""
超声波萃取设备 — 标准设备类模板 (Device Class Template)

定义「超声波萃取设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="ultrasonic_extractor",
    category=["超声波萃取设备"],
    description="超声波萃取设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="超声波萃取设备",
)
class UltrasonicExtractor:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "ultrasonic_extractor"
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

    @action(description="设置运行时间")
    def set_run_time(self, run_time: int = 0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[设置运行时间]: 设置运行时间。
        """
        pass

    @action(description="设置超声功率")
    def set_ultrasonic_power(self, ultrasonic_power: int = 0) -> Dict[str, Any]:
        """
        设置超声功率。

        Args:
            ultrasonic_power[设置超声功率]: 设置超声功率。
        """
        pass

    @action(description="设置超声频率")
    def set_ultrasonic_frequency(self, ultrasonic_frequency: int = 0) -> Dict[str, Any]:
        """
        设置超声频率。

        Args:
            ultrasonic_frequency[设置超声频率]: 设置超声频率。
        """
        pass

    @action(description="设置萃取温度")
    def set_extraction_temperature(self, extraction_temperature: int = 0) -> Dict[str, Any]:
        """
        设置萃取温度。

        Args:
            extraction_temperature[设置萃取温度]: 设置萃取温度。
        """
        pass

    @action(description="运行")
    def run(self) -> Dict[str, Any]:
        """运行。"""
        pass

    @action(description="停止")
    def stop(self) -> Dict[str, Any]:
        """停止。"""
        pass

    @action(description="复位")
    def reset(self) -> Dict[str, Any]:
        """复位。"""
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
    def ultrasonic_on_state(self) -> bool:
        """超声开启状态。"""
        return self.data.get("ultrasonic_on_state", False)

    @property
    @topic_config()
    def temperature_protection_state(self) -> bool:
        """温度保护状态。"""
        return self.data.get("temperature_protection_state", False)

    @property
    @topic_config()
    def liquid_level_state(self) -> bool:
        """液位检测状态。"""
        return self.data.get("liquid_level_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_run_time(self) -> int:
        """实际运行时间。"""
        return self.data.get("current_run_time", 0)

    @property
    @topic_config()
    def current_ultrasonic_power(self) -> int:
        """实际超声功率。"""
        return self.data.get("current_ultrasonic_power", 0)

    @property
    @topic_config()
    def current_ultrasonic_frequency(self) -> int:
        """实际超声频率。"""
        return self.data.get("current_ultrasonic_frequency", 0)

    @property
    @topic_config()
    def current_extraction_temperature(self) -> int:
        """实际萃取温度。"""
        return self.data.get("current_extraction_temperature", 0)
