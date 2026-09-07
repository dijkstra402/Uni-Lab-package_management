"""
抛光机 — 标准设备类模板 (Device Class Template)

定义「抛光机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="polishing_machine",
    category=["样品处理仪器与设备", "样品制备设备", "抛光机"],
    description="抛光机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="抛光机",
)
class PolishingMachine:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "polishing_machine"
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

    @action(description="设置抛光轮转速")
    def set_polishing_wheel_speed(self, polishing_wheel_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置抛光轮转速。

        Args:
            polishing_wheel_speed[抛光轮转速]: 目标抛光轮转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置抛光压力")
    def set_polishing_pressure(self, polishing_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置抛光压力。

        Args:
            polishing_pressure[抛光压力]: 目标抛光压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置抛光时间")
    def set_polishing_time(self, polishing_time: float = 0.0) -> Dict[str, Any]:
        """
        设置抛光时间。

        Args:
            polishing_time[抛光时间]: 目标抛光时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置抛光液流量")
    def set_polishing_fluid_flow(self, polishing_fluid_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置抛光液流量。

        Args:
            polishing_fluid_flow[抛光液流量]: 目标抛光液流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置样品转速")
    def set_sample_speed(self, sample_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置样品转速。

        Args:
            sample_speed[样品转速]: 目标样品转速（单位依设备量程而定）。
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

    @property
    @topic_config()
    def current_speed(self) -> float:
        """实际转速监测。"""
        return self.data.get("current_speed", 0.0)

    @property
    @topic_config()
    def polishing_precision_level(self) -> int:
        """抛光精度等级。"""
        return self.data.get("polishing_precision_level", 0)
