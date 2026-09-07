"""
研磨机 — 标准设备类模板 (Device Class Template)

定义「研磨机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="grinder",
    category=["样品处理仪器与设备", "表面处理设备", "研磨机"],
    description="研磨机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="研磨机",
)
class Grinder:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "grinder"
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

    @action(description="设置研磨盘转速")
    def set_grinding_disc_speed(self, grinding_disc_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨盘转速。

        Args:
            grinding_disc_speed[研磨盘转速]: 目标研磨盘转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置研磨压力")
    def set_grinding_pressure(self, grinding_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨压力。

        Args:
            grinding_pressure[研磨压力]: 目标研磨压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置研磨时间")
    def set_grinding_time(self, grinding_time: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨时间。

        Args:
            grinding_time[研磨时间]: 目标研磨时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置研磨粒度")
    def set_grinding_particle_size(self, grinding_particle_size: int = 0) -> Dict[str, Any]:
        """
        设置研磨粒度。

        Args:
            grinding_particle_size[研磨粒度]: 目标研磨粒度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置清洁时间")
    def set_cleaning_time(self, cleaning_time: float = 0.0) -> Dict[str, Any]:
        """
        设置清洁时间。

        Args:
            cleaning_time[清洁时间]: 目标清洁时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="研磨")
    def grind(self) -> Dict[str, Any]:
        """研磨。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="自动清洁")
    def auto_clean(self) -> Dict[str, Any]:
        """自动清洁。"""
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
    def grinding_disc_rotation_state(self) -> bool:
        """研磨盘旋转状态。"""
        return self.data.get("grinding_disc_rotation_state", False)

    @property
    @topic_config()
    def pressure_loading_state(self) -> bool:
        """压力加载状态。"""
        return self.data.get("pressure_loading_state", False)

    @property
    @topic_config()
    def cooling_system_running(self) -> bool:
        """冷却系统运行。"""
        return self.data.get("cooling_system_running", False)

    @property
    @topic_config()
    def guard_state(self) -> bool:
        """防护罩状态。"""
        return self.data.get("guard_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """实际转速检测。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_pressure(self) -> float:
        """实际压力检测。"""
        return self.data.get("current_pressure", 0.0)
