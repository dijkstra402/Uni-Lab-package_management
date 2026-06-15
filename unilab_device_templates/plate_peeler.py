"""
撕膜仪 — 标准设备类模板 (Device Class Template)

定义「撕膜仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="plate_peeler",
    category=["撕膜仪"],
    description="撕膜仪标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="撕膜仪",
)
class PlatePeeler:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "plate_peeler"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="撕膜启动")
    def start_peeling(self, mode: int = 0, peeling_speed: int = 0, peeling_height: int = 0, container_position: int = 0) -> Dict[str, Any]:
        """
        撕膜启动。

        Args:
            mode[运行模式设置]: 运行模式设置。
            peeling_speed[撕膜速度设置]: 撕膜速度设置。
            peeling_height[撕膜高度设置]: 撕膜高度设置。
            container_position[容器位置设置]: 容器位置设置。
        """
        pass

    @action(description="定位")
    def position(self, mode: int = 0, container_position: int = 0) -> Dict[str, Any]:
        """
        定位。

        Args:
            mode[运行模式设置]: 运行模式设置。
            container_position[容器位置设置]: 容器位置设置。
        """
        pass

    @action(description="抓取")
    def grip(self, mode: int = 0, grip_pressure: int = 0, container_position: int = 0) -> Dict[str, Any]:
        """
        抓取。

        Args:
            mode[运行模式设置]: 运行模式设置。
            grip_pressure[抓取压力设置]: 抓取压力设置。
            container_position[容器位置设置]: 容器位置设置。
        """
        pass

    @action(description="丢弃")
    def discard(self) -> Dict[str, Any]:
        """丢弃。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_peeling_speed(self) -> int:
        """实际撕膜速度。"""
        return self.data.get("current_peeling_speed", 0)

    @property
    @topic_config()
    def current_peeling_height(self) -> int:
        """实际撕膜高度。"""
        return self.data.get("current_peeling_height", 0)

    @property
    @topic_config()
    def current_grip_pressure(self) -> int:
        """实际抓取压力。"""
        return self.data.get("current_grip_pressure", 0)

    @property
    @topic_config()
    def current_container_position(self) -> int:
        """实际容器位置。"""
        return self.data.get("current_container_position", 0)
