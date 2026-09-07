"""
撕膜仪 — 标准设备类模板 (Device Class Template)

定义「撕膜仪」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="plate_peeler",
    category=["合成制备仪器与设备", "液体分配设备", "撕膜仪"],
    description="撕膜仪标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="撕膜仪",
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
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置撕膜速度")
    def set_peeling_speed(self, peeling_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置撕膜速度。

        Args:
            peeling_speed[撕膜速度]: 目标撕膜速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置撕膜高度")
    def set_peeling_height(self, peeling_height: float = 0.0) -> Dict[str, Any]:
        """
        设置撕膜高度。

        Args:
            peeling_height[撕膜高度]: 目标撕膜高度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置抓取压力")
    def set_grip_pressure(self, grip_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置抓取压力。

        Args:
            grip_pressure[抓取压力]: 目标抓取压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置容器位置")
    def set_container_position(self, container_position: float = 0.0) -> Dict[str, Any]:
        """
        设置容器位置。

        Args:
            container_position[容器位置]: 目标容器位置（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="撕膜启动")
    def start_peeling(self) -> Dict[str, Any]:
        """撕膜启动。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="定位")
    def position(self) -> Dict[str, Any]:
        """定位。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="抓取")
    def grip(self) -> Dict[str, Any]:
        """抓取。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="丢弃")
    def discard(self) -> Dict[str, Any]:
        """丢弃。"""
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
    def peeling_completed(self) -> bool:
        """撕膜完成。"""
        return self.data.get("peeling_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_peeling_speed(self) -> float:
        """实际撕膜速度。"""
        return self.data.get("current_peeling_speed", 0.0)

    @property
    @topic_config()
    def current_peeling_height(self) -> float:
        """实际撕膜高度。"""
        return self.data.get("current_peeling_height", 0.0)

    @property
    @topic_config()
    def current_grip_pressure(self) -> float:
        """实际抓取压力。"""
        return self.data.get("current_grip_pressure", 0.0)

    @property
    @topic_config()
    def current_container_position(self) -> float:
        """实际容器位置。"""
        return self.data.get("current_container_position", 0.0)
