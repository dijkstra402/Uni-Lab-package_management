"""
组织研磨仪 — 标准设备类模板 (Device Class Template)

定义「组织研磨仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="tissue_grinder",
    category=["样品处理仪器与设备", "表面处理设备", "组织研磨仪"],
    description="组织研磨仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="组织研磨仪",
)
class TissueGrinder:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "tissue_grinder"
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

    @action(description="设置目标转速")
    def set_target_speed(self, target_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置目标转速。

        Args:
            target_speed[目标转速]: 目标目标转速（单位依设备量程而定）。
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

    @action(description="设置振幅等级")
    def set_amplitude_level(self, amplitude_level: int = 0) -> Dict[str, Any]:
        """
        设置振幅等级。

        Args:
            amplitude_level[振幅等级]: 目标振幅等级（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置制冷温度")
    def set_cooling_temperature(self, cooling_temperature: float = 0.0) -> Dict[str, Any]:
        """
        设置制冷温度。

        Args:
            cooling_temperature[制冷温度]: 目标制冷温度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置循环次数")
    def set_cycle_count(self, cycle_count: int = 0) -> Dict[str, Any]:
        """
        设置循环次数。

        Args:
            cycle_count[循环次数]: 目标循环次数（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="研磨")
    def grind(self) -> Dict[str, Any]:
        """研磨。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="制冷")
    def cool(self) -> Dict[str, Any]:
        """制冷。"""
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
    def sample_chamber_door_state(self) -> bool:
        """样品室门状态。"""
        return self.data.get("sample_chamber_door_state", False)

    @property
    @topic_config()
    def safety_lock_state(self) -> bool:
        """安全锁状态。"""
        return self.data.get("safety_lock_state", False)

    @property
    @topic_config()
    def amplitude_stable_state(self) -> bool:
        """振幅稳定状态。"""
        return self.data.get("amplitude_stable_state", False)

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
    def current_temperature(self) -> float:
        """实际温度检测。"""
        return self.data.get("current_temperature", 0.0)
