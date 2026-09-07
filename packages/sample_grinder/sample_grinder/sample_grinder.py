"""
磨样机 — 标准设备类模板 (Device Class Template)

定义「磨样机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 未实现动作会抛出 NotImplementedError。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="sample_grinder",
    category=["样品处理仪器与设备", "样品制备设备", "磨样机"],
    description="磨样机标准接口：同一大类跨品牌统一的动作与参数。",
    displayname="磨样机",
)
class SampleGrinder:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "sample_grinder"
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

    @action(description="设置研磨转速")
    def set_grinding_speed(self, grinding_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨转速。

        Args:
            grinding_speed[研磨转速]: 目标研磨转速（单位依设备量程而定）。
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

    @action(description="设置研磨压力")
    def set_grinding_pressure(self, grinding_pressure: float = 0.0) -> Dict[str, Any]:
        """
        设置研磨压力。

        Args:
            grinding_pressure[研磨压力]: 目标研磨压力（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置磨头选择")
    def set_grinding_head_select(self, grinding_head_select: int = 0) -> Dict[str, Any]:
        """
        设置磨头选择。

        Args:
            grinding_head_select[磨头选择]: 目标磨头选择（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置粒度控制")
    def set_particle_size_control(self, particle_size_control: int = 0) -> Dict[str, Any]:
        """
        设置粒度控制。

        Args:
            particle_size_control[粒度控制]: 目标粒度控制（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置冷却水量")
    def set_cooling_water_volume(self, cooling_water_volume: int = 0) -> Dict[str, Any]:
        """
        设置冷却水量。

        Args:
            cooling_water_volume[冷却水量]: 目标冷却水量（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置振动频率")
    def set_vibration_frequency(self, vibration_frequency: float = 0.0) -> Dict[str, Any]:
        """
        设置振动频率。

        Args:
            vibration_frequency[振动频率]: 目标振动频率（单位依设备量程而定）。
        """
        raise NotImplementedError("请在设备包中实现该动作")

    @action(description="设置研磨精度")
    def set_grinding_precision(self, grinding_precision: int = 0) -> Dict[str, Any]:
        """
        设置研磨精度。

        Args:
            grinding_precision[研磨精度]: 目标研磨精度（单位依设备量程而定）。
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
