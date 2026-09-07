"""
分散机 — 标准设备类模板 (Device Class Template)

定义「分散机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="disperser",
    category=["样品处理仪器与设备", "混合与分散设备", "分散机"],
    description="分散机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="分散机",
)
class Disperser:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "disperser"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置分散转速")
    def set_dispersion_speed(self, dispersion_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置分散转速。

        Args:
            dispersion_speed[分散转速]: 目标分散转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置分散时间")
    def set_dispersion_time(self, dispersion_time: float = 0.0) -> Dict[str, Any]:
        """
        设置分散时间。

        Args:
            dispersion_time[分散时间]: 目标分散时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置分散头高度")
    def set_disperser_head_height(self, disperser_head_height: float = 0.0) -> Dict[str, Any]:
        """
        设置分散头高度。

        Args:
            disperser_head_height[分散头高度]: 目标分散头高度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置分散模式")
    def set_dispersion_mode(self, dispersion_mode: str = "") -> Dict[str, Any]:
        """
        设置分散模式。

        Args:
            dispersion_mode[分散模式]: 目标分散模式（具体取值由设备型号定义）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置转速增量")
    def set_speed_increment(self, speed_increment: float = 0.0) -> Dict[str, Any]:
        """
        设置转速增量。

        Args:
            speed_increment[转速增量]: 目标转速增量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置增量时间")
    def set_increment_time(self, increment_time: float = 0.0) -> Dict[str, Any]:
        """
        设置增量时间。

        Args:
            increment_time[增量时间]: 目标增量时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置扭矩限制")
    def set_torque_limit(self, torque_limit: float = 0.0) -> Dict[str, Any]:
        """
        设置扭矩限制。

        Args:
            torque_limit[扭矩限制]: 目标扭矩限制（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="分散")
    def disperse(self) -> Dict[str, Any]:
        """分散。"""
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
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)

    @property
    @topic_config()
    def current_speed(self) -> float:
        """当前转速显示。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def current_time(self) -> float:
        """当前时间显示。"""
        return self.data.get("current_time", 0.0)

    @property
    @topic_config()
    def current_height(self) -> float:
        """当前高度显示。"""
        return self.data.get("current_height", 0.0)

    @property
    @topic_config()
    def current_torque(self) -> float:
        """当前扭矩显示。"""
        return self.data.get("current_torque", 0.0)
