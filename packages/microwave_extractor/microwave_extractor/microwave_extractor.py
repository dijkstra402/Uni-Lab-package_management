"""
微波萃取设备 — 标准设备类模板 (Device Class Template)

定义「微波萃取设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="microwave_extractor",
    category=["微波萃取设备"],
    description="微波萃取设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="微波萃取设备",
)
class MicrowaveExtractor:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "microwave_extractor"
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

    @action(description="设置运行时间")
    def set_run_time(self, run_time: float = 0.0) -> Dict[str, Any]:
        """
        设置运行时间。

        Args:
            run_time[运行时间]: 目标运行时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置微波功率")
    def set_microwave_power(self, microwave_power: float = 0.0) -> Dict[str, Any]:
        """
        设置微波功率。

        Args:
            microwave_power[微波功率]: 目标微波功率（单位依设备量程而定）。
        """
        pass

    @action(description="设置萃取温度")
    def set_extraction_temperature(self, extraction_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置萃取温度。

        Args:
            extraction_temperature[萃取温度]: 目标萃取温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置搅拌速度")
    def set_stir_speed(self, stir_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置搅拌速度。

        Args:
            stir_speed[搅拌速度]: 目标搅拌速度（单位依设备量程而定）。
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
    def pressure_protection_state(self) -> bool:
        """压力保护状态。"""
        return self.data.get("pressure_protection_state", False)

    @property
    @topic_config()
    def temperature_protection_state(self) -> bool:
        """温度保护状态。"""
        return self.data.get("temperature_protection_state", False)

    @property
    @topic_config()
    def microwave_on_state(self) -> bool:
        """微波开启状态。"""
        return self.data.get("microwave_on_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_run_time(self) -> float:
        """实际运行时间。"""
        return self.data.get("current_run_time", 0.0)

    @property
    @topic_config()
    def current_microwave_power(self) -> float:
        """实际微波功率。"""
        return self.data.get("current_microwave_power", 0.0)

    @property
    @topic_config()
    def current_extraction_temperature(self) -> float:
        """实际萃取温度。"""
        return self.data.get("current_extraction_temperature", 0.0)

    @property
    @topic_config()
    def current_stir_speed(self) -> float:
        """实际搅拌速度。"""
        return self.data.get("current_stir_speed", 0.0)
