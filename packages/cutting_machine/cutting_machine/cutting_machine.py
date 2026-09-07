"""
切割机 — 标准设备类模板 (Device Class Template)

定义「切割机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="cutting_machine",
    category=["样品处理仪器与设备", "样品制备设备", "切割机"],
    description="切割机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="切割机",
)
class CuttingMachine:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "cutting_machine"
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

    @action(description="设置切割速度")
    def set_cutting_speed(self, cutting_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置切割速度。

        Args:
            cutting_speed[切割速度]: 目标切割速度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置切割深度")
    def set_cutting_depth(self, cutting_depth: float = 0.0) -> Dict[str, Any]:
        """
        设置切割深度。

        Args:
            cutting_depth[切割深度]: 目标切割深度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置进给速率")
    def set_feed_rate(self, feed_rate: float = 0.0) -> Dict[str, Any]:
        """
        设置进给速率。

        Args:
            feed_rate[进给速率]: 目标进给速率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置切割压力")
    def set_cutting_pressure(self, cutting_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置切割压力。

        Args:
            cutting_pressure[切割压力]: 目标切割压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置冷却液流量")
    def set_coolant_flow(self, coolant_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置冷却液流量。

        Args:
            coolant_flow[冷却液流量]: 目标冷却液流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置刀片转速")
    def set_blade_speed(self, blade_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置刀片转速。

        Args:
            blade_speed[刀片转速]: 目标刀片转速（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置切割精度")
    def set_cutting_precision(self, cutting_precision: int = 0) -> Dict[str, Any]:
        """
        设置切割精度。

        Args:
            cutting_precision[切割精度]: 目标切割精度（单位依设备量程而定）。
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
