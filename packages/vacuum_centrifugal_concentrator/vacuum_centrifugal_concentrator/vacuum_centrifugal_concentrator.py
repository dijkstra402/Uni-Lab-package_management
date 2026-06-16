"""
真空离心浓缩仪 — 标准设备类模板 (Device Class Template)

定义「真空离心浓缩仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="vacuum_centrifugal_concentrator",
    category=["真空离心浓缩仪"],
    description="真空离心浓缩仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="真空离心浓缩仪",
)
class VacuumCentrifugalConcentrator:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "vacuum_centrifugal_concentrator"
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

    @action(description="设置转速")
    def set_speed(self, speed: float = 0.0) -> Dict[str, Any]:
        """
        设置转速。

        Args:
            speed[转速]: 目标转速（单位依设备量程而定）。
        """
        pass

    @action(description="浓缩")
    def concentrate(self) -> Dict[str, Any]:
        """浓缩。"""
        pass

    @action(description="真空")
    def vacuum(self) -> Dict[str, Any]:
        """真空。"""
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
    def current_speed(self) -> float:
        """实际转速。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def vacuum(self) -> float:
        """真空度。"""
        return self.data.get("vacuum", 0.0)

    @property
    @topic_config()
    def concentration_temperature(self) -> float:
        """浓缩温度。"""
        return self.data.get("concentration_temperature", 0.0)

    @property
    @topic_config()
    def concentration_time(self) -> float:
        """浓缩时间。"""
        return self.data.get("concentration_time", 0.0)

    @property
    @topic_config()
    def heating_power(self) -> float:
        """加热功率。"""
        return self.data.get("heating_power", 0.0)
