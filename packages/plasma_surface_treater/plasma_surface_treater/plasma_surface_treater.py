"""
等离子体表面处理机 — 标准设备类模板 (Device Class Template)

定义「等离子体表面处理机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="plasma_surface_treater",
    category=["样品处理仪器与设备", "样品制备设备", "等离子体表面处理机"],
    description="等离子体表面处理机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="等离子体表面处理机",
)
class PlasmaSurfaceTreater:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "plasma_surface_treater"
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

    @action(description="设置处理功率")
    def set_treatment_power(self, treatment_power: float = 0.0) -> Dict[str, Any]:
        """
        设置处理功率。

        Args:
            treatment_power[处理功率]: 目标处理功率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置处理时间")
    def set_treatment_time(self, treatment_time: float = 0.0) -> Dict[str, Any]:
        """
        设置处理时间。

        Args:
            treatment_time[处理时间]: 目标处理时间（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置真空度")
    def set_vacuum(self, vacuum: float = 0.0) -> Dict[str, Any]:
        """
        设置真空度。

        Args:
            vacuum[真空度]: 目标真空度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置气体流量")
    def set_gas_flow(self, gas_flow: float = 0.0) -> Dict[str, Any]:
        """
        设置气体流量。

        Args:
            gas_flow[气体流量]: 目标气体流量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置电极距离")
    def set_electrode_distance(self, electrode_distance: float = 0.0) -> Dict[str, Any]:
        """
        设置电极距离。

        Args:
            electrode_distance[电极距离]: 目标电极距离（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置等离子体密度")
    def set_plasma_density(self, plasma_density: float = 0.0) -> Dict[str, Any]:
        """
        设置等离子体密度。

        Args:
            plasma_density[等离子体密度]: 目标等离子体密度（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置处理次数")
    def set_treatment_count(self, treatment_count: int = 0) -> Dict[str, Any]:
        """
        设置处理次数。

        Args:
            treatment_count[处理次数]: 目标处理次数（单位依设备量程而定）。
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
    def sample_moving_speed(self) -> float:
        """样品移动速度。"""
        return self.data.get("sample_moving_speed", 0.0)
