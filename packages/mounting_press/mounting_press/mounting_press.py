"""
镶嵌机 — 标准设备类模板 (Device Class Template)

定义「镶嵌机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="mounting_press",
    category=["镶嵌机"],
    description="镶嵌机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="镶嵌机",
)
class MountingPress:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "mounting_press"
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

    @action(description="设置加热温度")
    def set_heating_temperature(self, heating_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置加热温度。

        Args:
            heating_temperature[加热温度]: 目标加热温度（单位依设备量程而定）。
        """
        pass

    @action(description="设置加热时间")
    def set_heating_time(self, heating_time: float = 0.0) -> Dict[str, Any]:
        """
        设置加热时间。

        Args:
            heating_time[加热时间]: 目标加热时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置冷却时间")
    def set_cooling_time(self, cooling_time: float = 0.0) -> Dict[str, Any]:
        """
        设置冷却时间。

        Args:
            cooling_time[冷却时间]: 目标冷却时间（单位依设备量程而定）。
        """
        pass

    @action(description="设置压力")
    def set_pressure(self, pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置压力。

        Args:
            pressure[压力]: 目标压力（单位依设备量程而定）。
        """
        pass

    @action(description="设置保温时间")
    def set_holding_time(self, holding_time: float = 0.0) -> Dict[str, Any]:
        """
        设置保温时间。

        Args:
            holding_time[保温时间]: 目标保温时间（单位依设备量程而定）。
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
    def running_completed(self) -> bool:
        """运行完成。"""
        return self.data.get("running_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)
