"""
激光清洗机 — 标准设备类模板 (Device Class Template)

定义「激光清洗机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="laser_cleaner",
    category=["样品处理仪器与设备", "清洗机", "激光清洗机"],
    description="激光清洗机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="激光清洗机",
)
class LaserCleaner:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "laser_cleaner"
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

    @action(description="设置清洗时间")
    def set_cleaning_time(self, cleaning_time: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗时间。

        Args:
            cleaning_time[清洗时间]: 目标清洗时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置清洗温度")
    def set_cleaning_temperature(self, cleaning_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗温度。

        Args:
            cleaning_temperature[清洗温度]: 目标清洗温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置清洗压力")
    def set_cleaning_pressure(self, cleaning_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置清洗压力。

        Args:
            cleaning_pressure[清洗压力]: 目标清洗压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置激光功率")
    def set_laser_power(self, laser_power: float = 0.0) -> Dict[str, Any]:
        """
        设置激光功率。

        Args:
            laser_power[激光功率]: 目标激光功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置扫描速度")
    def set_scan_speed(self, scan_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置扫描速度。

        Args:
            scan_speed[扫描速度]: 目标扫描速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置聚焦距离")
    def set_focus_distance(self, focus_distance: float = 0.0) -> Dict[str, Any]:
        """
        设置聚焦距离。

        Args:
            focus_distance[聚焦距离]: 目标聚焦距离（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="清洗准备")
    def prepare_cleaning(self) -> Dict[str, Any]:
        """清洗准备。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="清洗结束")
    def finish_cleaning(self) -> Dict[str, Any]:
        """清洗结束。"""
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
    def laser_head_moving_state(self) -> bool:
        """激光头移动状态。"""
        return self.data.get("laser_head_moving_state", False)

    @property
    @topic_config()
    def cooling_system_state(self) -> bool:
        """冷却系统状态。"""
        return self.data.get("cooling_system_state", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_cleaning_time(self) -> float:
        """实际清洗时间。"""
        return self.data.get("current_cleaning_time", 0.0)

    @property
    @topic_config()
    def laser_power_feedback(self) -> float:
        """激光功率反馈。"""
        return self.data.get("laser_power_feedback", 0.0)

    @property
    @topic_config()
    def scan_speed_feedback(self) -> float:
        """扫描速度反馈。"""
        return self.data.get("scan_speed_feedback", 0.0)

    @property
    @topic_config()
    def focus_distance_feedback(self) -> float:
        """聚焦距离反馈。"""
        return self.data.get("focus_distance_feedback", 0.0)
