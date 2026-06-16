"""
微波消解仪 — 标准设备类模板 (Device Class Template)

定义「微波消解仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="microwave_digester",
    category=["微波消解仪"],
    description="微波消解仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="微波消解仪",
)
class MicrowaveDigester:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "microwave_digester"
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

    @action(description="设置目标温度")
    def set_target_temperature(self, target_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置目标温度。

        Args:
            target_temperature[目标温度]: 目标目标温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置目标压力")
    def set_target_pressure(self, target_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置目标压力。

        Args:
            target_pressure[目标压力]: 目标目标压力（单位依设备量程而定）。
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

    @action(description="设置消解时间")
    def set_digestion_time(self, digestion_time: float = 0.0) -> Dict[str, Any]:
        """
        设置消解时间。

        Args:
            digestion_time[消解时间]: 目标消解时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置程序段")
    def set_program_segment(self, program_segment: int = 0) -> Dict[str, Any]:
        """
        设置程序段。

        Args:
            program_segment[程序段]: 目标程序段（单位依设备量程而定）。
        """
        pass

    @action(description="消解")
    def digest(self) -> Dict[str, Any]:
        """消解。"""
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
    def microwave_output_state(self) -> bool:
        """微波输出状态。"""
        return self.data.get("microwave_output_state", False)

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
    def chamber_door_off_state(self) -> bool:
        """腔门关闭状态。"""
        return self.data.get("chamber_door_off_state", False)

    @property
    @topic_config()
    def cooling_system_running(self) -> bool:
        """冷却系统运行。"""
        return self.data.get("cooling_system_running", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_temperature(self) -> float:
        """实际温度检测。"""
        return self.data.get("current_temperature", 0.0)

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """实际压力检测。"""
        return self.data.get("current_pressure", 0.0)
