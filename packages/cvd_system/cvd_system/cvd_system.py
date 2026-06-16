"""
化学气相沉积设备 — 标准设备类模板 (Device Class Template)

定义「化学气相沉积设备」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="cvd_system",
    category=["化学气相沉积设备"],
    description="化学气相沉积设备标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="化学气相沉积设备",
)
class CvdSystem:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "cvd_system"
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

    @action(description="设置沉积温度")
    def set_deposition_temperature(self, deposition_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置沉积温度。

        Args:
            deposition_temperature[沉积温度]: 目标沉积温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置工艺压力")
    def set_process_pressure(self, process_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置工艺压力。

        Args:
            process_pressure[工艺压力]: 目标工艺压力（单位依设备量程而定）。
        """
        pass

    @action(description="设置气体流量 1 ")
    def set_gas_flow_1(self, gas_flow_1: float = 0.0) -> Dict[str, Any]:
        """
        设置气体流量 1 。

        Args:
            gas_flow_1[气体流量 1 ]: 目标气体流量 1 （单位依设备量程而定）。
        """
        pass

    @action(description="设置沉积时间")
    def set_deposition_time(self, deposition_time: float = 0.0) -> Dict[str, Any]:
        """
        设置沉积时间。

        Args:
            deposition_time[沉积时间]: 目标沉积时间（单位依设备量程而定）。
        """
        pass

    @action(description="沉积启动")
    def start_deposition(self) -> Dict[str, Any]:
        """沉积启动。"""
        pass

    @action(description="抽真空")
    def evacuate(self) -> Dict[str, Any]:
        """抽真空。"""
        pass

    @action(description="气体切换")
    def switch_gas(self) -> Dict[str, Any]:
        """气体切换。"""
        pass

    @action(description="降温")
    def cool_down(self) -> Dict[str, Any]:
        """降温。"""
        pass

    @action(description="腔室开门")
    def open_chamber_door(self) -> Dict[str, Any]:
        """腔室开门。"""
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
    def deposition_completed(self) -> bool:
        """沉积完成。"""
        return self.data.get("deposition_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_deposition_temperature(self) -> float:
        """沉积温度实际值。"""
        return self.data.get("current_deposition_temperature", 0.0)

    @property
    @topic_config()
    def current_process_pressure(self) -> float:
        """工艺压力实际值。"""
        return self.data.get("current_process_pressure", 0.0)

    @property
    @topic_config()
    def current_gas_flow_1(self) -> float:
        """气体流量 1 实际值。"""
        return self.data.get("current_gas_flow_1", 0.0)

    @property
    @topic_config()
    def deposition_time_remaining(self) -> float:
        """沉积时间剩余值。"""
        return self.data.get("deposition_time_remaining", 0.0)
