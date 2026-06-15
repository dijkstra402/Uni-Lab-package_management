"""
组织研磨仪 — 标准设备类模板 (Device Class Template)

定义「组织研磨仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="tissue_grinder",
    category=["组织研磨仪"],
    description="组织研磨仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="组织研磨仪",
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
        pass

    @action(description="研磨")
    def grind(self, mode: int = 0, target_speed: int = 0, grinding_time: int = 0, amplitude_level: int = 0, cycle_count: int = 0) -> Dict[str, Any]:
        """
        研磨。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_speed[目标转速设置]: 目标转速设置。
            grinding_time[研磨时间设置]: 研磨时间设置。
            amplitude_level[振幅等级设置]: 振幅等级设置。
            cycle_count[循环次数设置]: 循环次数设置。
        """
        pass

    @action(description="制冷")
    def cool(self, mode: int = 0, target_speed: int = 0, amplitude_level: int = 0, cooling_temperature: int = 0, cycle_count: int = 0) -> Dict[str, Any]:
        """
        制冷。

        Args:
            mode[运行模式设置]: 运行模式设置。
            target_speed[目标转速设置]: 目标转速设置。
            amplitude_level[振幅等级设置]: 振幅等级设置。
            cooling_temperature[制冷温度设置]: 制冷温度设置。
            cycle_count[循环次数设置]: 循环次数设置。
        """
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
    def current_speed(self) -> int:
        """实际转速检测。"""
        return self.data.get("current_speed", 0)

    @property
    @topic_config()
    def current_temperature(self) -> int:
        """实际温度检测。"""
        return self.data.get("current_temperature", 0)
