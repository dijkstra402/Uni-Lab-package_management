"""
均胶机 — 标准设备类模板 (Device Class Template)

定义「均胶机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="spin_coater",
    category=["样品处理仪器与设备", "样品制备设备", "匀胶机"],
    description="均胶机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="均胶机",
)
class SpinCoater:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "spin_coater"
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

    @action(description="设置低速时间")
    def set_low_speed_time(self, low_speed_time: float = 0.0) -> Dict[str, Any]:
        """
        设置低速时间。

        Args:
            low_speed_time[低速时间]: 目标低速时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置高速时间")
    def set_high_speed_time(self, high_speed_time: float = 0.0) -> Dict[str, Any]:
        """
        设置高速时间。

        Args:
            high_speed_time[高速时间]: 目标高速时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置加速度")
    def set_acceleration(self, acceleration: float = 0.0) -> Dict[str, Any]:
        """
        设置加速度。

        Args:
            acceleration[加速度]: 目标加速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置减速度")
    def set_deceleration(self, deceleration: float = 0.0) -> Dict[str, Any]:
        """
        设置减速度。

        Args:
            deceleration[减速度]: 目标减速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置样品尺寸")
    def set_sample_size(self, sample_size: int = 0) -> Dict[str, Any]:
        """
        设置样品尺寸。

        Args:
            sample_size[样品尺寸]: 目标样品尺寸（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
    def running_completed(self) -> bool:
        """运行完成。"""
        return self.data.get("running_completed", False)

    @property
    @topic_config()
    def fault_code(self) -> int:
        """故障代码。"""
        return self.data.get("fault_code", 0)
