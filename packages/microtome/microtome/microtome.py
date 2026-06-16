"""
切片机 — 标准设备类模板 (Device Class Template)

定义「切片机」这一设备大类的标准动作(action)与状态属性(property)。
同一大类下不同品牌的设备都应实现这套统一接口，使一套工作流可跨品牌控制整类设备。

注意: 本文件只定义标准接口, 方法体为 pass(占位)。真实实现由各品牌驱动继承/对接。
来源: 电气通讯协议标准化 device_action_spec.json
"""

from typing import Any, Dict, Optional

from unilabos.registry.decorators import device, action, topic_config


@device(
    id="microtome",
    category=["切片机"],
    description="切片机标准接口：同一大类跨品牌统一的动作与参数。",
    display_name="切片机",
)
class Microtome:

    def __init__(self, device_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        初始化设备。

        Args:
            device_id[设备ID]: 设备实例 ID。
            config[设备配置]: 设备启动配置。
        """
        self.device_id = device_id or "microtome"
        self.config = config or {}
        self.data: Dict[str, Any] = {"status": "idle"}

    @action(description="初始化")
    def initialize(self) -> Dict[str, Any]:
        """初始化。"""
        pass

    @action(description="设置运行模式")
    def set_mode(self, mode: str = "") -> Dict[str, Any]:
        """
        设置运行模式。

        Args:
            mode[运行模式]: 目标运行模式（具体取值由设备型号定义）。
        """
        pass

    @action(description="设置切片厚度")
    def set_slice_thickness(self, slice_thickness: float = 0.0) -> Dict[str, Any]:
        """
        设置切片厚度。

        Args:
            slice_thickness[切片厚度]: 目标切片厚度（单位依设备量程而定）。
        """
        pass

    @action(description="设置切片速度")
    def set_slice_speed(self, slice_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置切片速度。

        Args:
            slice_speed[切片速度]: 目标切片速度（单位依设备量程而定）。
        """
        pass

    @action(description="设置进给量")
    def set_feed_amount(self, feed_amount: int = 0) -> Dict[str, Any]:
        """
        设置进给量。

        Args:
            feed_amount[进给量]: 目标进给量（单位依设备量程而定）。
        """
        pass

    @action(description="设置刀架角度")
    def set_tool_holder_angle(self, tool_holder_angle: float = 0.0) -> Dict[str, Any]:
        """
        设置刀架角度。

        Args:
            tool_holder_angle[刀架角度]: 目标刀架角度（单位依设备量程而定）。
        """
        pass

    @action(description="设置样品转速")
    def set_sample_speed(self, sample_speed: float = 0.0) -> Dict[str, Any]:
        """
        设置样品转速。

        Args:
            sample_speed[样品转速]: 目标样品转速（单位依设备量程而定）。
        """
        pass

    @action(description="设置切片精度")
    def set_slice_precision(self, slice_precision: int = 0) -> Dict[str, Any]:
        """
        设置切片精度。

        Args:
            slice_precision[切片精度]: 目标切片精度（单位依设备量程而定）。
        """
        pass

    @action(description="设置切片数量")
    def set_slicing_count(self, slicing_count: int = 0) -> Dict[str, Any]:
        """
        设置切片数量。

        Args:
            slicing_count[切片数量]: 目标切片数量（单位依设备量程而定）。
        """
        pass

    @action(description="启动")
    def start(self) -> Dict[str, Any]:
        """启动。"""
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
    def slicing_interval_time(self) -> float:
        """切片间隔时间。"""
        return self.data.get("slicing_interval_time", 0.0)
