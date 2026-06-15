"""
激光清洗机 — 标准设备类模板 (Device Class Template)

定义「激光清洗机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="laser_cleaner",
    category=["激光清洗机"],
    description="激光清洗机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="激光清洗机",
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
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: int = 0) -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[设置运行模式]: 设置运行模式。
        """
        pass

    @action(description="设置清洗温度")
    def set_cleaning_temperature(self, cleaning_temperature: int = 0) -> Dict[str, Any]:
        """
        设置清洗温度。

        Args:
            cleaning_temperature[设置清洗温度]: 设置清洗温度。
        """
        pass

    @action(description="设置清洗压力")
    def set_qing_xi_pressure(self, qing_xi_pressure: int = 0) -> Dict[str, Any]:
        """
        设置清洗压力。

        Args:
            qing_xi_pressure[设置清洗压力]: 设置清洗压力。
        """
        pass

    @action(description="设置激光功率")
    def set_laser_power(self, laser_power: int = 0) -> Dict[str, Any]:
        """
        设置激光功率。

        Args:
            laser_power[设置激光功率]: 设置激光功率。
        """
        pass

    @action(description="设置扫描速度")
    def set_scan_speed(self, scan_speed: int = 0) -> Dict[str, Any]:
        """
        设置扫描速度。

        Args:
            scan_speed[设置扫描速度]: 设置扫描速度。
        """
        pass

    @action(description="设置聚焦距离")
    def set_focus_distance(self, focus_distance: int = 0) -> Dict[str, Any]:
        """
        设置聚焦距离。

        Args:
            focus_distance[设置聚焦距离]: 设置聚焦距离。
        """
        pass

    @action(description="清洗")
    def clean(self) -> Dict[str, Any]:
        """清洗。"""
        pass

    @action(description="清洗准备")
    def prepare_cleaning(self) -> Dict[str, Any]:
        """清洗准备。"""
        pass

    @action(description="清洗结束")
    def finish_cleaning(self) -> Dict[str, Any]:
        """清洗结束。"""
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
    def laser_head_yi_dong_state(self) -> bool:
        """激光头移动状态。"""
        return self.data.get("laser_head_yi_dong_state", False)

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
    def current_cleaning_time(self) -> int:
        """实际清洗时间。"""
        return self.data.get("current_cleaning_time", 0)

    @property
    @topic_config()
    def laser_power_feedback(self) -> int:
        """激光功率反馈。"""
        return self.data.get("laser_power_feedback", 0)

    @property
    @topic_config()
    def scan_speed_feedback(self) -> int:
        """扫描速度反馈。"""
        return self.data.get("scan_speed_feedback", 0)

    @property
    @topic_config()
    def focus_distance_feedback(self) -> int:
        """聚焦距离反馈。"""
        return self.data.get("focus_distance_feedback", 0)
